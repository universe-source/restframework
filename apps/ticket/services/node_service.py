"""
Node Service
"""
import logging
from django.db import transaction
from django.db.models import Q

import errors
from customs import BaseService, BaseSerializer
from apps.config import Config
from ..models import TicketNode
from ..serializers import TicketNodeSerializer


logger = logging.getLogger('ticket')


class TicketNodeService(BaseService, BaseSerializer):
    model = TicketNode
    serializer_class = TicketNodeSerializer
    desc = 'Ticket Node object serialize'

    def find_children(self, root_name):
        """Find all child by root_name"""
        root = self.get_or_none(name=root_name)
        children = root.children.keys()

        if children:
            return set([root])

        nodes = set([])
        for child in children:
            nodes.union(self.find_children(child))
        return nodes

    def find_root(self, tid, **kwargs):
        """Find root node by ticket_type id"""
        roots = self.filter(tid=tid, defaults="")
        if roots:
            if len(roots) == 1:
                return True, roots[0]
            return False, errors.CODE_TOO_MANY_TICKET_ROOT_NODE

        num = 0
        root_name = ''
        for name, value in kwargs.items():
            if not value.get('default', ''):
                num += 1
                root_name = name

        if num == 1:
            root = self.create_node(
                tid, root_name, '', kwargs.pop(root_name))
            return True, root
        elif num == 0:
            return False, errors.CODE_LEAK_TICKET_ROOT_NODE
        return False, errors.CODE_TOO_MANY_TICKET_ROOT_NODE

    def serialize_tree(self, tid, root, nodes=None):
        """Serialize a tree data accross by root node"""
        if not nodes:
            nodes = self.filter(tid=tid).filter(~Q(parent=''))
        return {
            'root': root,
            'nodes': self.serializes(nodes)
        }

    def create_node(self, tid, name, parent, **kwargs):
        """Create a ticket node"""
        children_values = {child: {} for child in kwargs.get('children', [])}
        node = self.update_or_create(
            name=name, tid=tid,
            default={
                'alias': kwargs.get('alias', ''),
                'parent': parent,
                'children': children_values
            })
        return node

    @transaction.atomic
    def add_subtree(self, tid, root, subroot=None, **kwargs):
        unroot_nodes_name = root.children.keys()
        if subroot:
            if subroot not in unroot_nodes_name:
                root.children[subroot.name] = {}
                root.save()
                unroot_nodes_name.append(subroot.name)

        nodes = []
        existed_parents = [root.name]
        for name in unroot_nodes_name:
            value = kwargs.pop(name)
            parent = value.get('parent')
            if parent in existed_parents:
                node = self.create_node(tid, name, parent, value)
                if node:
                    existed_parents.append(parent)
                    nodes.append(node)
                    continue
                return False, errors.CODE_CREATE_TICKET_NODE_FAILED
            return False, errors.CODE_VALID_FORMAT_TICKET_NODE
        return True, root

    @transaction.atomic
    def delete_subtree(self, subroot):
        node = self.get_or_none(name=subroot)
        if node:
            parent_node = self.get_or_none(name=node.parent)
            parent_node.children.pop(node.name)
            parent_node.save()

            children_nodes = self.find_children(node.name)
            children_ids = [child_node.id for child_node in children_nodes]
            self.filter(id__in=children_ids).delete()

            return self.find_root(node.tid)
        return False, errors.CODE_UNEXIST_TICKET_NODE

    @transaction.atomic
    def move_subtree(self, tid, src, dst, subroot):
        src_node = self.get_or_none(name=src)
        dst_node = self.get_or_none(name=dst)
        sub_node = self.get_or_none(name=subroot)
        if src_node and dst_node and sub_node:
            if subroot.name in src_node.children:
                dst_node.children[subroot] = src_node.children[subroot]
                src_node.children.pop(subroot)
                sub_node.parent = dst_node.name
                src_node.save()
                dst_node.save()
                sub_node.save()
                return self.find_root(tid)
        return False, errors.CODE_UNEXIST_TICKET_NODE

    @transaction.atomic
    def update_or_create_tree(self, ticket_type, **kwargs):
        """
        @input:
            {
                "node1": {
                    "alias": "node1 alias",
                    "parent": "",
                    "children": {
                        ...
                    }
                },
                ...
            }
        @function: find root and update all existed child node
        """
        succ, root = self.find_root(ticket_type.id, **kwargs)
        if succ:
            return self.add_subtree(ticket_type.id, root, **kwargs)
        return False, root


ticket_node_service = TicketNodeService()
