# -*- coding: utf-8 -*-

import logging
from openerp import models, fields, osv, exceptions, api

_logger = logging.getLogger(__name__)
# This component is invoked regularly (see data/cron.xml for details) 
# to perform the "refresh" of models which reflects external entities
# like cloud resources, repos information etc. Since several models
# are involved (and new models can be created from these refreshes)
# we have created this component for this purpose (instead of call
# operations on regular models)
class Refresher(models.Model):
    _name = 'unison.refresher'
    _auto = False # This settings avoids the creation of a table 

    # This function is used to refresh the cloud-related models
    # which doesn't have frequent changes (like list of regions,
    # list of sizes, list of images etc)
    @api.model
    def cloud_cold_refresh(self):
        # Right now we only have support for just one cloud
        cloud = self.env['unison.cloud']
        clouds = cloud.search([('code', '=', 'digitalocean')])
        cloud_id = clouds[0].id

        # Refresh Regions
        print "Refreshing Regions..."
        digital_ocean = self.env['unison.digital_ocean']
        regions = digital_ocean.get_regions()
        for regionItem in regions:
            code = regionItem['slug']
            region = self.env['unison.region']
            regions = region.search([('code', '=', code)])
            if len(regions) == 0:
                # Create region
                region = region.create({
                    'code': regionItem['slug'], 
                    'name': regionItem['name'],
                    'cloud_id': cloud_id,
                    'available': regionItem['available'],
                    'notes': '',
                    'active': True
                })
            else:
                # Update 'available' field
                region = region.search([('code', '=', code)])
                region.write({
                    'available': regionItem['available'],
                })

        # Refresh Sizes
        print "Refreshing Sizes..."
        digital_ocean = self.env['unison.digital_ocean']
        sizes = digital_ocean.get_sizes()
        for sizeItem in sizes:
            code = sizeItem['slug']
            size = self.env['unison.size']
            sizes = size.search([('code', '=', code)])
            if len(sizes) == 0:
                # Create size
                size = size.create({
                    'code': sizeItem['slug'], 
                    'name': sizeItem['slug'], # Size doesn't have a friendly name, but we can edit it
                    'cloud_id': cloud_id,
                    'ram_mb': sizeItem['memory'],
                    'cpu_cores': sizeItem['vcpus'],
                    'disk_gb': sizeItem['disk'],
                    'transfer_tb': sizeItem['transfer'],
                    'available': sizeItem['available'],
                    'hourly_price_usd': sizeItem['price_hourly'],
                    'notes': '',
                    'active': True
                })
            else:
                # Update available status
                size = size.search([('code', '=', code)])
                region.write({
                    'available': sizeItem['available'],
                })


        print "Process completed"

        return True

    # This function is used to refresh the cloud-related models
    # which have frequent changes due our own changes related
    # to the launching of new installations etc.
    @api.model
    def cloud_hot_refresh(self):
        return True

    # This function is used to refresh the information about
    # registered repos (branches, modules, etc)
    @api.model
    def repos_refresh(self):
        return True
