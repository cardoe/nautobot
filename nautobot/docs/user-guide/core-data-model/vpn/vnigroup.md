# VNI Groups

VNI groups can be used to organize [VPNs](vpn.md) by their VXLAN Network Identifier (VNI) and to constrain which VNIs are valid. Each group may optionally be assigned to a single [Location](../dcim/location.md), restricting the VNIs that are permitted there — much as a [VLAN Group](../ipam/vlangroup.md) restricts VLAN IDs.

A group also enforces uniqueness: each VPN within a group must have a unique VNI. VPNs that are not assigned to a group may reuse VNIs freely.

## VNI Group Ranges

VNI Groups contain a mandatory `range` field with a default value of `1-16777214` (permitting all valid VXLAN VNIs). This field constrains the valid member VPNs of the group: a VPN can only be associated with a VNI Group if its identifier (`vpn_id`) is a numeric VNI that falls within the specified `range`.

The range value accepts commas and dashes, for example:

* `100`
* `100-200`
* `100-200,300`
* `100-200,300-400,500`

Values between dashes are expanded into the full list of VNIs.

## Restricting VNIs at a Location

Assign a VNI Group to a Location to declare which VNIs are valid there. A VPN scoped to that group inherits the restriction transitively: its VNI must fall within the group's permitted range, and the group's Location must be of a [Location Type](../dcim/locationtype.md) that permits VNI groups.

## Validation Rules

- When a VNI Group is assigned to a VPN, the VPN's identifier (`vpn_id`) is required and must be a numeric VNI contained within the group's `range`.
- A group's `range` may not be resized so as to exclude the VNI of an existing member VPN.
- A group may only be assigned to a Location whose Location Type permits VNI groups.
