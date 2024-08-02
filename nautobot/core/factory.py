from ipaddress import IPv6Address, IPV6LENGTH, IPv6Network
import itertools

from django.core.exceptions import ValidationError
from django.db.models import Model
import factory
from factory.django import DjangoModelFactory
from factory.errors import FactoryError
import factory.random
from faker.providers import BaseProvider

from nautobot.core import constants
from nautobot.extras.models import Tag


class UniqueFaker(factory.Faker):
    """https://github.com/FactoryBoy/factory_boy/pull/820#issuecomment-1004802669"""

    @classmethod
    def _get_faker(cls, locale=None):
        return super()._get_faker(locale=locale).unique

    def clear(self, locale=None):
        subfaker = self._get_faker(locale)
        subfaker.clear()


class BaseModelFactory(DjangoModelFactory):
    """Base class for all Nautobot model factories."""

    id = UniqueFaker("uuid4")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override default DjangoModelFactory behavior to call validated_save() instead of just save()."""
        if cls._meta.django_get_or_create:
            return cls._get_or_create(model_class, *args, **kwargs)

        using = kwargs.pop("using", cls._meta.database)
        obj = model_class(*args, **kwargs)
        try:
            obj.validated_save(using=using)
        except ValidationError as err:
            print(f"Got a ValidationError for {obj}: {err}")
            raise
        return obj

    @classmethod
    def _get_or_create(cls, model_class, *args, **kwargs):
        """Simplified form of DjangoModelFactory._get_or_create() that also calls validated_save() if needed."""
        using = kwargs.pop("using", cls._meta.database)
        key_fields = {}
        for field in cls._meta.django_get_or_create:
            if field not in kwargs:
                raise FactoryError(f"no value provided for field {field}")
            key_fields[field] = kwargs.pop(field)

        try:
            obj = model_class.objects.using(using).get(*args, **key_fields)
        except model_class.DoesNotExist:
            obj = model_class(*args, **key_fields, **kwargs)
            try:
                obj.validated_save(using=using)
            except ValidationError as err:
                print(f"Got a ValidationError for {obj}: {err}")
                raise

        return obj


class OrganizationalModelFactory(BaseModelFactory):
    """Factory base class for OrganizationalModel subclasses."""

    # TODO random created/last_updated values?
    # TODO random custom_field data?
    # TODO random relationships?
    # TODO random dynamic-groups?
    # TODO random notes?


class PrimaryModelFactory(BaseModelFactory):
    """Factory base class for PrimaryModel subclasses."""

    # TODO random created/last_updated values?
    # TODO random custom_field data?
    # TODO random relationships?
    # TODO random dynamic-groups?
    # TODO random notes?

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if create:
            if extracted:
                self.tags.set(extracted)
            else:
                self.tags.set(get_random_instances(Tag.objects.get_for_model(self._meta.model)))


def _get_queryset_from_model_or_queryset_or_lambda(model_or_queryset_or_lambda):
    """
    Get a queryset object given an input which may be a model class OR queryset OR lambda function that returns either.

    This makes it possible for us to do any of the following:

    random_instance(Location)
    random_instance(Location.objects.filter(...))
    random_instance(lambda: Location)
    random_instance(lambda: Location.objects.get_for_model(...))
    """
    if isinstance(model_or_queryset_or_lambda, type) and issubclass(model_or_queryset_or_lambda, Model):
        queryset = model_or_queryset_or_lambda.objects.all()
    elif callable(model_or_queryset_or_lambda):
        model_or_queryset = model_or_queryset_or_lambda()
        if isinstance(model_or_queryset, type) and issubclass(model_or_queryset, Model):
            queryset = model_or_queryset.objects.all()
        else:
            queryset = model_or_queryset
    else:
        queryset = model_or_queryset_or_lambda

    return queryset


def random_instance(model_or_queryset_or_lambda, allow_null=True):
    """
    Factory helper - construct a LazyFunction that gets a random instance of the given model or queryset when evaluated.

    TODO: once we have factories for all mandatory foreign keys, change allow_null default to False

    Args:
        model_or_queryset_or_lambda (Union[BaseModel, QuerySet, func]): Either a model class, a model queryset, or a lambda that returns one of those
        allow_null (bool): If False, and the given queryset contains no objects, raise a RuntimeError.

    Example:
        class ObjectFactory(DjangoModelFactory):
            class Meta:
                model = Object
                exclude = ("has_group,")

            # Required foreign key
            user = random_instance(User, allow_null=False)

            # Optional foreign key
            has_group = NautobotBoolIterator()
            group = factory.Maybe("has_group", random_instance(Group), None)

            # Foreign key selected from a filtered queryset
            tenant = random_instance(Tenant.objects.filter(group__isnull=False))

            # Foreign key selected from a queryset generated by a lambda
            # This needs to be done this way because .get_for_model() evaluates a ContentType queryset,
            # and we need to defer evaluation of that queryset as well.
            status = random_instance(lambda: Status.objects.get_for_model(Object), allow_null=False)
    """

    def get_random_instance():
        queryset = _get_queryset_from_model_or_queryset_or_lambda(model_or_queryset_or_lambda)

        if not allow_null and not queryset.exists():
            raise RuntimeError(f"No objects in queryset for {model_or_queryset_or_lambda}! {queryset.explain()}")

        return factory.random.randgen.choice(queryset) if queryset.exists() else None

    return factory.LazyFunction(get_random_instance)


def get_random_instances(model_or_queryset_or_lambda, minimum=0, maximum=None):
    """
    Factory helper - retrieve a random number of instances of the given model.

    This is different from random_instance() in that it's not itself a lazy function generator, but should instead be
    called only from within a @lazy_attribute or @post_generation function.

    This is not an evenly weighted distribution (all counts equally likely), because in most of our code,
    the relevant code paths distinguish between 0, 1, or >1 instances - there's not a functional difference between
    "2 instances" and "10 instances" in most cases. Therefore, this implementation provides:
        - 1/3 chance of no instances
        - 1/3 chance of 1 instance
        - 1/3 chance of (2 to n) instances, where each possibility is equally likely within this range

    Args:
        model_or_queryset_or_lambda (Union[BaseModel, QuerySet, func]): Either a model class, a model queryset, or a lambda that returns one of those
        minimum (int): Minimum number of objects to return
        maximum (int): Maximum number of objects to return, or None for no limit
    """
    branch = factory.random.randgen.randint(0, 2)
    queryset = _get_queryset_from_model_or_queryset_or_lambda(model_or_queryset_or_lambda)
    count = queryset.count()
    if maximum is None:
        maximum = count
    if any([branch == 0 and minimum == 0, count == 0, maximum == 0]):
        return []
    if any([branch == 1 and minimum <= 1, count == 1, maximum == 1]):
        return [factory.random.randgen.choice(queryset)]
    return factory.random.randgen.sample(
        population=list(queryset),
        k=factory.random.randgen.randint(max(2, minimum), min(maximum, count)),
    )


class NautobotBoolIterator(factory.Iterator):
    """Factory iterator that returns a semi-random sampling of boolean values

    Iterator that returns a random sampling of True and False values while limiting
    the number of repeated values in a given number of iterations. Used in factories
    when a data set must contain both True and False values.

    Args:
        cycle (boolean): If True, iterator will restart at the beginning when all values are
            exhausted. Otherwise raise a `StopIterator` exception when values are exhausted.
            Defaults to True.
        chance_of_getting_true (int): Percentage (0-100) of the values in the returned iterable
            set to True. Defaults to 50.
        length (int): Length of the returned iterable. Defaults to 8.
    """

    def _nautobot_boolean_iterator_sample(self, chance_of_getting_true, length):
        iterator = list(itertools.repeat(True, int(length * chance_of_getting_true / 100)))
        iterator += list(itertools.repeat(False, length - len(iterator)))
        factory.random.randgen.shuffle(iterator)
        return iterator

    def __init__(
        self,
        *args,
        cycle=True,
        getter=None,
        chance_of_getting_true=constants.NAUTOBOT_BOOL_ITERATOR_DEFAULT_PROBABILITY,
        length=constants.NAUTOBOT_BOOL_ITERATOR_DEFAULT_LENGTH,
    ):
        super().__init__(None, cycle=cycle, getter=getter)

        if cycle:
            self.iterator_builder = lambda: factory.utils.ResetableIterator(
                itertools.cycle(self._nautobot_boolean_iterator_sample(chance_of_getting_true, length))
            )
        else:
            self.iterator_builder = lambda: factory.utils.ResetableIterator(
                self._nautobot_boolean_iterator_sample(chance_of_getting_true, length)
            )


class NautobotFakerProvider(BaseProvider):
    """Faker provider to generate fake data specific to Nautobot or network automation use cases."""

    def ipv6_network(self) -> str:
        """Produce a random IPv6 network with a valid CIDR greater than 0"""
        address = str(IPv6Address(self.generator.random.randint(0, (2**IPV6LENGTH) - 1)))
        address += "/" + str(self.generator.random.randint(1, IPV6LENGTH))
        address = str(IPv6Network(address, strict=False))
        return address


factory.Faker.add_provider(NautobotFakerProvider)
