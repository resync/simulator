#!/usr/bin/env python

"""inventory.py: A ResourceSync inventory contains a set of resources. This
module contains all inventory-related operations"""

__author__      = "Bernhard Haslhofer"
__copyright__   = "Copyright 2012, ResourceSync.org"

import pprint
import random

import util

DEFAULT_RESOURCES = 100
"""The default number of resources created at bootstrap"""
MAX_PAYLOAD_SIZE = 500
"""The maximum payload size (in bytes)"""

class Inventory:
    """An inventory holds a set of resources and keeps track of changes."""
    
    def __init__(self, no_resources = DEFAULT_RESOURCES):
        """Initializes and fills the resource inventory at startup time"""
        self.current_resources = {} # current inventory
        self.deleted_resources = {} # holds deletion history
        self.updated_resources = {} # holds update history
        self.max_res_id = 0
        print '*** Bootstrapping inventory with %d seed resources ***\n' \
                % no_resources
        for i in range(no_resources): self.create_resource()
    
    def select_random_resource(self):
        """Selects a random resource id from the inventory"""
        if len(self.current_resources.keys()) > 0:
            return random.choice(self.current_resources.keys())
        else:
            return None
    
    def create_resource(self, res_id = None):
        """Creates a new resource, add it to the inventory, and return it"""
        if res_id == None:
            res_id = self.max_res_id # assign a new id
            self.max_res_id += 1
        res = dict(
            id = res_id,
            lm = util.current_datetime(),
            pl = util.generate_payload(MAX_PAYLOAD_SIZE)
        )
        self.current_resources[res_id] = res
        return res
    
    def update_resource(self, res_id):
        """Updates a resource with given a given resource id and return it"""
        old_res = self.current_resources[res_id]
        new_res = self.create_resource(res_id)
        self.updated_resources[res_id] = old_res
        return new_res
        
    def delete_resource(self, res_id):
        """Deletes a resource with a given resource id and return it"""
        res = self.current_resources[res_id]
        self.deleted_resources[res_id] = res
        del self.current_resources[res_id]
        return res
    
    # Inventory serialization functions
    
    def __str__(self):
        """Prints out the current simulator inventory as string"""
        cr = "INVENTORY:\n" + pprint.pformat(self.current_resources)
        dr = "DELETED RESOURCES:\n" + pprint.pformat(self.deleted_resources)
        ur = "UPDATED RESOURCES:\n" + pprint.pformat(self.updated_resources)
        return cr + "\n" + dr + "\n" + ur
        
    def to_sitemap(self):
        """Serializes the inventory to a sitemap"""
        pass
        
if __name__ == '__main__':
    inventory = Inventory(10)
    print inventory