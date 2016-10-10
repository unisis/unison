# -*- coding: utf-8 -*-

import datetime
import logging
import dateutil.parser as dateparser
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

        # Refresh Actions (from last action)
        print "UNISON: Refreshing Actions..."
        digital_ocean = self.env['unison.digital_ocean']

        date_last = self.query_scalar("SELECT MAX(date_end) FROM unison_action")
        if date_last == None:
            after = ''
        else:
            # We will retrieve from one second after last event
            time_parsed = dateparser.parse(date_last)
            time_seconds = time_parsed.strftime('%s')
            time_seconds = int(time_seconds) + 1
            date_time = datetime.datetime.utcfromtimestamp(time_seconds)
            after = date_time.isoformat("T") + "Z"

        actions = digital_ocean.get_actions(after) # We only retrieve new actions
        for actionItem in actions:
            # Create action

            if 'region' in actionItem.keys():
                region_code = actionItem['region']['slug']
                region = self.env['unison.region']
                region = region.search([('code', '=', region_code)])
                region_id = region.id
            else:
                region_id = None

            action = self.env['unison.action']
            action = action.create({
                'code': actionItem['id'],
                'type': actionItem['type'],
                'status': actionItem['status'],
                'date_start': actionItem['started_at'],
                'date_end': actionItem['completed_at'],
                'resource_type': actionItem['resource_type'],
                'resource_code': actionItem['resource_id'],
                'region_id': region_id
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

            # Refresh Records of this domain
            print "UNISON: Refreshing records for domain " + name + "..."
            digital_ocean = self.env['unison.digital_ocean']
            records = digital_ocean.get_records(name)
            for recordItem in records:
                code = recordItem['id']
                record = self.env['unison.record']
                record = record.search([('code', '=', code)])
                if len(record) > 0:
                    # Update record
                    record.write({
                        'type': recordItem['type'],
                        'name': recordItem['name'],
                        'content': recordItem['data'],
                    })
                else:
                    # Create record
                    print "UNISON: Creating record"

                    # Priority field is only available on certain records
                    if 'priority' in recordItem.keys():
                        priority = recordItem['priority']
                    else:
                        priority = None

                    record = record.create({
                        'code': recordItem['id'], 
                        'type': recordItem['type'],
                        'name': recordItem['name'],
                        'content': recordItem['data'],
                        'priority': priority,
                        'domain_id': domain.id,
                        'notes': '',
                        'active': True
                    })

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

        # Refresh Floating IPs
        print "UNISON: Refreshing Floating IPs..."
        digital_ocean = self.env['unison.digital_ocean']
        floating_ips = digital_ocean.get_floating_ips()
        for floatingItem in floating_ips:
            address = floatingItem['ip']
            region_code = floatingItem['region']['slug']
            region = self.env['unison.region']
            region = region.search([('code', '=', region_code)])
            region_id = region.id

            # Check if floating ip is attached to node
            if floatingItem['droplet'] == None:
                node_id = None
            else:
                droplet = floatingItem['droplet']
                node = self.env['unison.node']
                node = node.search([('code', '=', droplet['id'])])
                node_id = node.id

            floating_ip = self.env['unison.floating_ip']
            floating_ip = floating_ip.search([('address', '=', address)])
            if len(floating_ip) > 0:
                # Update info about the floating ip (attach info)
                floating_ip.write({
                    'node_id': node_id,
                })
            else:
                # Create floating ip
                print "UNISON: Creating floating ip " + address
                floating_ip = floating_ip.create({
                    'address': address,
                    'region_id': region_id,
                    'node_id': node_id,
                    'notes': '',
                    'active': True
                })

        # Refresh Volumes
        print "UNISON: Refreshing Volumes..."
        digital_ocean = self.env['unison.digital_ocean']
        volumes = digital_ocean.get_volumes()
        for volumeItem in volumes:
            code = volumeItem['id']
            region_code = volumeItem['region']['slug']
            region = self.env['unison.region']
            region = region.search([('code', '=', region_code)])
            region_id = region.id

            # Check if volume is attached to node
            if len(volumeItem['droplet_ids']) == 0:
                node_id = None
            else:
                droplet_code = volumeItem['droplet_ids'][0]
                node = self.env['unison.node']
                node = node.search([('code', '=', droplet_code)])
                node_id = node.id

            volume = self.env['unison.volume']
            volume = volume.search([('code', '=', code)])
            if len(volume) > 0:
                # Update info about the volume (attach info and size)
                volume.write({
                    'node_id': node_id,
                    'size_gb': volumeItem['size_gigabytes']
                })
            else:
                # Create volume
                print "UNISON: Creating volume " + code
                volume = volume.create({
                    'code': code,
                    'name': volumeItem['name'],
                    'size_gb': volumeItem['size_gigabytes'],
                    'region_id': region_id,
                    'node_id': node_id,
                    'filesystem': None, # Will be provided by UniSon
                    'mount_point': None, # Will be provided by UniSon
                    'notes': '',
                    'active': True
                })

        print "UNISON: Process completed"

        return True

    # This function is used to refresh the information about
    # registered repos (branches, modules, etc)
    @api.model
    def repos_refresh(self):
        return True

    # This function is a wrapper to perform a query and return a scalar value
    def query_scalar(self, query):
        self.env.cr.execute(query)
        result = self.env.cr.fetchall()
        if result == None:
            return None
        row = result[0]
        for value in row:
            return value


