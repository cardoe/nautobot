from nautobot.core.apps import (
    NavContext,
    NavGrouping,
    NavItem,
    NavMenuAddButton,
    NavMenuGroup,
    NavMenuItem,
    NavMenuImportButton,
    NavMenuTab,
)


menu_items = (
    NavMenuTab(
        name="IPAM",
        weight=300,
        groups=(
            NavMenuGroup(
                name="IP Addresses",
                weight=100,
                items=(
                    NavMenuItem(
                        link="ipam:ipaddress_list",
                        name="IP Addresses",
                        weight=100,
                        permissions=[
                            "ipam.view_ipaddress",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="ipam:ipaddress_add",
                                permissions=[
                                    "ipam.add_ipaddress",
                                ],
                            ),
                            NavMenuImportButton(
                                link="ipam:ipaddress_import",
                                permissions=[
                                    "ipam.add_ipaddress",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="ipam:ipaddresstointerface_import",
                        name="IP Address Assignments",
                        weight=200,
                        permissions=[
                            "ipam.add_ipaddresstointerface",
                        ],
                        buttons=(
                            NavMenuImportButton(
                                link="ipam:ipaddresstointerface_import",
                                permissions=[
                                    "ipam.add_ipaddresstointerface",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
            NavMenuGroup(
                name="Prefixes",
                weight=200,
                items=(
                    NavMenuItem(
                        link="ipam:prefix_list",
                        name="Prefixes",
                        weight=100,
                        permissions=[
                            "ipam.view_prefix",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="ipam:prefix_add",
                                permissions=[
                                    "ipam.add_prefix",
                                ],
                            ),
                            NavMenuImportButton(
                                link="ipam:prefix_import",
                                permissions=[
                                    "ipam.add_prefix",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
            NavMenuGroup(
                name="RIRs",
                weight=300,
                items=(
                    NavMenuItem(
                        link="ipam:rir_list",
                        name="RIRs",
                        weight=200,
                        permissions=[
                            "ipam.view_rir",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="ipam:rir_add",
                                permissions=[
                                    "ipam.add_rir",
                                ],
                            ),
                            NavMenuImportButton(
                                link="ipam:rir_import",
                                permissions=[
                                    "ipam.add_rir",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
            NavMenuGroup(
                name="VRFs",
                weight=400,
                items=(
                    NavMenuItem(
                        link="ipam:namespace_list",
                        name="Namespaces",
                        weight=100,
                        permissions=[
                            "ipam.view_namespace",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="ipam:namespace_add",
                                permissions=[
                                    "ipam.add_namespace",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="ipam:vrf_list",
                        name="VRFs",
                        weight=100,
                        permissions=[
                            "ipam.view_vrf",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="ipam:vrf_add",
                                permissions=[
                                    "ipam.add_vrf",
                                ],
                            ),
                            NavMenuImportButton(
                                link="ipam:vrf_import",
                                permissions=[
                                    "ipam.add_vrf",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="ipam:routetarget_list",
                        name="Route Targets",
                        weight=200,
                        permissions=[
                            "ipam.view_routetarget",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="ipam:routetarget_add",
                                permissions=[
                                    "ipam.add_routetarget",
                                ],
                            ),
                            NavMenuImportButton(
                                link="ipam:routetarget_import",
                                permissions=[
                                    "ipam.add_routetarget",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
            NavMenuGroup(
                name="VLANs",
                weight=500,
                items=(
                    NavMenuItem(
                        link="ipam:vlan_list",
                        name="VLANs",
                        weight=100,
                        permissions=[
                            "ipam.view_vlan",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="ipam:vlan_add",
                                permissions=[
                                    "ipam.add_vlan",
                                ],
                            ),
                            NavMenuImportButton(
                                link="ipam:vlan_import",
                                permissions=[
                                    "ipam.add_vlan",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="ipam:vlangroup_list",
                        name="VLAN Groups",
                        weight=200,
                        permissions=[
                            "ipam.view_vlangroup",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="ipam:vlangroup_add",
                                permissions=[
                                    "ipam.add_vlangroup",
                                ],
                            ),
                            NavMenuImportButton(
                                link="ipam:vlangroup_import",
                                permissions=[
                                    "ipam.add_vlangroup",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
            NavMenuGroup(
                name="Services",
                weight=600,
                items=(
                    NavMenuItem(
                        link="ipam:service_list",
                        name="Services",
                        weight=100,
                        permissions=[
                            "ipam.view_service",
                        ],
                        buttons=(
                            NavMenuImportButton(
                                link="ipam:service_import",
                                permissions=[
                                    "ipam.add_service",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
)


navigation = (
    NavContext(
        name="Networks",
        groups=(
            NavGrouping(
                name="IP Management",
                weight=100,
                items=(
                    NavItem(
                        name="IP Addresses",
                        weight=100,
                        link="ipam:ipaddress_list",
                        permissions=["ipam.view_ipaddress"],
                    ),
                    NavItem(
                        name="Prefixes",
                        weight=200,
                        link="ipam:prefix_list",
                        permissions=["ipam.view_prefix"],
                    ),
                    NavItem(
                        name="RIRs",
                        weight=300,
                        link="ipam:rir_list",
                        permissions=["ipam.view_rir"],
                    ),
                ),
            ),
            NavGrouping(
                name="Layer 2 / Switching",
                weight=200,
                items=(
                    NavItem(
                        name="VLANs",
                        weight=100,
                        link="ipam:vlan_list",
                        permissions=["ipam.view_vlan"],
                    ),
                    NavItem(
                        name="VLAN Groups",
                        weight=200,
                        link="ipam:vlangroup_list",
                        permissions=["ipam.view_vlangroup"],
                    ),
                ),
            ),
            NavGrouping(
                name="Layer 3 / Routing",
                weight=300,
                items=(
                    NavItem(
                        name="Namespaces",
                        weight=100,
                        link="ipam:namespace_list",
                        permissions=["ipam.view_namespace"],
                    ),
                    NavItem(
                        name="VRFs",
                        weight=200,
                        link="ipam:vrf_list",
                        permissions=["ipam.view_vrf"],
                    ),
                    NavItem(
                        name="Route Targets",
                        weight=300,
                        link="ipam:routetarget_list",
                        permissions=["ipam.view_routetarget"],
                    ),
                ),
            ),
            NavGrouping(
                name="Services",
                weight=400,
                items=(
                    NavItem(
                        name="Services",
                        weight=100,
                        link="ipam:service_list",
                        permissions=["ipam.view_service"],
                    ),
                ),
            ),
        ),
    ),
)
