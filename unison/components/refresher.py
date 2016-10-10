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
        print "UNISON: Refreshing Regions..."
        digital_ocean = self.env['unison.digital_ocean']
        regions = digital_ocean.get_regions()
        for regionItem in regions:
            code = regionItem['slug']
            region = self.env['unison.region']
            regions = region.search([('code', '=', code)])
            if len(regions) > 0:
                # Update 'available' field
                region = region.search([('code', '=', code)])
                region.write({
                    'available': regionItem['available'],
                })
            else:
                # Create region
                print "UNISON: Creating region " + code
                region = region.create({
                    'code': regionItem['slug'], 
                    'name': regionItem['name'],
                    'cloud_id': cloud_id,
                    'available': regionItem['available'],
                    'notes': '',
                    'active': True
                })

            # Refresh Features
            for featureItem in regionItem['features']:
                code = featureItem
                feature = self.env['unison.feature']
                feature = feature.search([('code', '=', code)])
                if len(feature) == 0:
                    # Create new feature
                    print "UNISON: Creating feature " + code
                    feature = feature.create({
                        'code': code, 
                        'cloud_id': cloud_id,
                        'notes': '',
                        'active': True
                    })
                region.feature_ids += feature

        # Refresh Sizes
        print "UNISON: Refreshing Sizes..."
        digital_ocean = self.env['unison.digital_ocean']
        sizes = digital_ocean.get_sizes()
        for sizeItem in sizes:
            code = sizeItem['slug']
            size = self.env['unison.size']
            sizes = size.search([('code', '=', code)])
            if len(sizes) > 0:
                # Update available status
                size = size.search([('code', '=', code)])
                size.write({
                    'available': sizeItem['available'],
                })
            else:
                # Create size
                print "UNISON: Creating size " + code
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

            # Update regions where this size is available
            regions = sizeItem['regions']
            for regionCode in regions:
                region = self.env['unison.region']
                region = region.search([('code', '=', regionCode)])
                if region.id != False:
                    size.region_ids += region

        # Refresh Images
        print "UNISON: Refreshing Images..."
        digital_ocean = self.env['unison.digital_ocean']
        images = digital_ocean.get_images()
        for imageItem in images:
            code = imageItem['id']
            image = self.env['unison.image']
            image = image.search([('code', '=', code)])
            if len(image) == 0:
                # Create image
                print "UNISON: Creating image " + imageItem['name']

                is_backup = (imageItem['type'] != 'snapshot')
                if 'public' in imageItem.keys():
                    is_private = (imageItem['public'] == False)
                else:
                    # Private snapshots doesn't have the 'public' item
                    is_private = True
                
                image = image.create({
                    'code': imageItem['id'], 
                    'name': imageItem['name'],
                    'cloud_id': cloud_id,
                    'is_backup': is_backup,
                    'is_private': is_private,
                    'min_disk_size': imageItem['min_disk_size'],
                    'distribution': imageItem['distribution'],
                    'created_at': imageItem['created_at'],
                    'notes': '',
                    'active': True
                })

            # Refresh regions where this image is available
            regions = imageItem['regions']
            for regionCode in regions:
                region = self.env['unison.region']
                region = region.search([('code', '=', regionCode)])
                if region.id != False:
                    image.region_ids += region

        print "UNISON: Process completed"

        return True

    # This function is used to refresh the cloud-related models
    # which have frequent changes due our own changes related
    # to the launching of new installations etc.
    @api.model
    def cloud_hot_refresh(self):
        # Right now we only have support for just one cloud
        cloud = self.env['unison.cloud']
        clouds = cloud.search([('code', '=', 'digitalocean')])
        cloud_id = clouds[0].id

        # Refresh Keys
        print "UNISON: Refreshing Keys..."
        digital_ocean = self.env['unison.digital_ocean']
        keys = digital_ocean.get_keys()
        for keyItem in keys:
            fingerprint = keyItem['fingerprint']
            key = self.env['unison.key']
            key = key.search([('fingerprint', '=', fingerprint)])
            if len(key) > 0:
                # Indicate that this key was added to DigitalOcean
                key.write({
                    'code': keyItem['id'],
                    'name': keyItem['name'],
                    'cloud_id': cloud_id,
                })
            else:
                # Create key
                print "UNISON: Creating key " + fingerprint
                key = key.create({
                    'code': keyItem['id'], 
                    'name': keyItem['name'],
                    'cloud_id': cloud_id,
                    'fingerprint': keyItem['fingerprint'],
                    'public_key': keyItem['public_key'],
                    'private_key': '', # This information should be provided manually
                    'putty_key': '', # This information should be provided manually
                    'notes': '',
                    'active': True
                })

        # Refresh Domains
        print "UNISON: Refreshing Domains..."
        digital_ocean = self.env['unison.digital_ocean']
        domains = digital_ocean.get_domains()
        for domainItem in domains:
            name = domainItem['name']
            domain = self.env['unison.domain']
            domain = domain.search([('name', '=', name)])
            if len(domain) > 0:
                # Update their zone file
                domain.write({
                    'zone_file': domainItem['zone_file'],
                })
            else:
                # Create domain
                print "UNISON: Creating domain " + name
                domain = domain.create({
                    'name': domainItem['name'],
                    'cloud_id': cloud_id,
                    'ttl': domainItem['ttl'],
                    'zone_file': domainItem['zone_file'],
                    'notes': '',
                    'active': True
                })

        return True

    # This function is used to refresh the information about
    # registered repos (branches, modules, etc)
    @api.model
    def repos_refresh(self):
        return True
