# -*- coding: utf-8 -*-

import os
import datetime
import logging
import subprocess
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
        for region_item in regions:
            code = region_item['slug']
            region = self.env['unison.region']
            regions = region.search([('code', '=', code)])
            if len(regions) > 0:
                # Update 'available' field
                region = region.search([('code', '=', code)])
                region.write({
                    'available': region_item['available'],
                })
            else:
                # Create region
                print "UNISON: Creating region " + code
                region = region.create({
                    'code': region_item['slug'], 
                    'name': region_item['name'],
                    'cloud_id': cloud_id,
                    'available': region_item['available'],
                    'notes': '',
                    'active': True
                })

            # Refresh Features
            for feature_item in region_item['features']:
                code = feature_item
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
        for size_item in sizes:
            code = size_item['slug']
            size = self.env['unison.size']
            sizes = size.search([('code', '=', code)])
            if len(sizes) > 0:
                # Update available status
                size = size.search([('code', '=', code)])
                size.write({
                    'available': size_item['available'],
                })
            else:
                # Create size
                print "UNISON: Creating size " + code
                size = size.create({
                    'code': size_item['slug'], 
                    'name': size_item['slug'], # Size doesn't have a friendly name, but we can edit it
                    'cloud_id': cloud_id,
                    'ram_mb': size_item['memory'],
                    'cpu_cores': size_item['vcpus'],
                    'disk_gb': size_item['disk'],
                    'transfer_tb': size_item['transfer'],
                    'available': size_item['available'],
                    'hourly_price_usd': size_item['price_hourly'],
                    'notes': '',
                    'active': True
                })

            # Update regions where this size is available
            regions = size_item['regions']
            for region_code in regions:
                region = self.env['unison.region']
                region = region.search([('code', '=', region_code)])
                if region.id != False:
                    size.region_ids += region

        # Refresh Images
        print "UNISON: Refreshing Images..."
        digital_ocean = self.env['unison.digital_ocean']
        images = digital_ocean.get_images()
        for image_item in images:
            code = image_item['id']
            image = self.env['unison.image']
            image = image.search([('code', '=', code)])
            if len(image) == 0:
                # Create image
                print "UNISON: Creating image " + image_item['name']

                is_backup = (image_item['type'] != 'snapshot')
                if 'public' in image_item.keys():
                    is_private = (image_item['public'] == False)
                else:
                    # Private snapshots doesn't have the 'public' item
                    is_private = True
                
                image = image.create({
                    'code': image_item['id'], 
                    'name': image_item['name'],
                    'cloud_id': cloud_id,
                    'is_backup': is_backup,
                    'is_private': is_private,
                    'min_disk_size': image_item['min_disk_size'],
                    'distribution': image_item['distribution'],
                    'created_at': image_item['created_at'],
                    'notes': '',
                    'active': True
                })

            # Refresh regions where this image is available
            regions = image_item['regions']
            for region_code in regions:
                region = self.env['unison.region']
                region = region.search([('code', '=', region_code)])
                if region.id != False:
                    image.region_ids += region

        print "UNISON: Completed cold refresh of clouds"

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
        for action_item in actions:
            # Create action

            if 'region' in action_item.keys():
                region_code = action_item['region']['slug']
                region = self.env['unison.region']
                region = region.search([('code', '=', region_code)])
                region_id = region.id
            else:
                region_id = None

            action = self.env['unison.action']
            action = action.create({
                'code': action_item['id'],
                'type': action_item['type'],
                'status': action_item['status'],
                'date_start': action_item['started_at'],
                'date_end': action_item['completed_at'],
                'resource_type': action_item['resource_type'],
                'resource_code': action_item['resource_id'],
                'region_id': region_id
            })

        # Refresh Domains
        print "UNISON: Refreshing Domains..."
        digital_ocean = self.env['unison.digital_ocean']
        domains = digital_ocean.get_domains()
        for domain_item in domains:
            name = domain_item['name']
            domain = self.env['unison.domain']
            domain = domain.search([('name', '=', name)])
            if len(domain) > 0:
                # Update their zone file
                domain.write({
                    'zone_file': domain_item['zone_file'],
                })
            else:
                # Create domain
                print "UNISON: Creating domain " + name
                domain = domain.create({
                    'name': domain_item['name'],
                    'cloud_id': cloud_id,
                    'ttl': domain_item['ttl'],
                    'zone_file': domain_item['zone_file'],
                    'notes': '',
                    'active': True
                })

            # Refresh Records of this domain
            print "UNISON: Refreshing records for domain " + name + "..."
            digital_ocean = self.env['unison.digital_ocean']
            records = digital_ocean.get_records(name)
            for record_item in records:
                code = record_item['id']
                record = self.env['unison.record']
                record = record.search([('code', '=', code)])
                if len(record) > 0:
                    # Update record
                    record.write({
                        'type': record_item['type'],
                        'name': record_item['name'],
                        'content': record_item['data'],
                    })
                else:
                    # Create record
                    print "UNISON: Creating record"

                    # Priority field is only available on certain records
                    if 'priority' in record_item.keys():
                        priority = record_item['priority']
                    else:
                        priority = None

                    record = record.create({
                        'code': record_item['id'], 
                        'type': record_item['type'],
                        'name': record_item['name'],
                        'content': record_item['data'],
                        'priority': priority,
                        'domain_id': domain.id,
                        'notes': '',
                        'active': True
                    })

        # Refresh Keys
        print "UNISON: Refreshing Keys..."
        digital_ocean = self.env['unison.digital_ocean']
        keys = digital_ocean.get_keys()
        for key_item in keys:
            fingerprint = key_item['fingerprint']
            key = self.env['unison.key']
            key = key.search([('fingerprint', '=', fingerprint)])
            if len(key) > 0:
                # Indicate that this key was added to DigitalOcean
                key.write({
                    'code': key_item['id'],
                    'name': key_item['name'],
                    'cloud_id': cloud_id,
                })
            else:
                # Create key
                print "UNISON: Creating key " + fingerprint
                key = key.create({
                    'code': key_item['id'], 
                    'name': key_item['name'],
                    'cloud_id': cloud_id,
                    'fingerprint': key_item['fingerprint'],
                    'public_key': key_item['public_key'],
                    'private_key': '', # This information should be provided manually
                    'putty_key': '', # This information should be provided manually
                    'notes': '',
                    'active': True
                })

        # Refresh Nodes
        print "UNISON: Refreshing Nodes..."
        digital_ocean = self.env['unison.digital_ocean']
        nodes = digital_ocean.get_nodes()
        for node_item in nodes:
            code = node_item['id']

            # Get region_id
            region_code = node_item['region']['slug']
            region = self.env['unison.region']
            region = region.search([('code', '=', region_code)])
            region_id = region.id

            # Get size_id
            size_code = node_item['size']['slug']
            size = self.env['unison.size']
            size = size.search([('code', '=', size_code)])
            size_id = size.id

            # Get image_id
            image_code = node_item['image']['id']
            image = self.env['unison.image']
            image = image.search([('code', '=', image_code)])
            image_id = image.id

            # Get IPv4 network info
            public_ip = None
            private_ip = None
            for network in node_item['networks']['v4']:
                if network['type'] == 'public':
                    public_ip = network['ip_address']
                else:
                    private_ip = network['ip_address']

            node = self.env['unison.node']
            node = node.search([('code', '=', code)])
            if len(node) > 0:
                # Update node info
                node.write({
                    'size_id': size_id,
                    'public_ip': public_ip,
                    'private_ip': private_ip,
                    'status': node_item['status'],
                })
            else:
                # Create node
                print "UNISON: Creating node " + str(code)
                node = node.create({
                    'code': code, 
                    'name': node_item['name'],
                    'image_id': image_id,
                    'size_id': size_id,
                    'region_id': region_id,
                    'key_id': None,   # TO-DO ASSIGN
                    'record_id': None, # TO-DO ASSIGN
                    'public_ip': public_ip,
                    'private_ip': private_ip,
                    'status': node_item['status'],
                    'notes': '',
                    'active': True
                })

        # Refresh Floating IPs
        print "UNISON: Refreshing Floating IPs..."
        digital_ocean = self.env['unison.digital_ocean']
        floating_ips = digital_ocean.get_floating_ips()
        for floating_item in floating_ips:
            address = floating_item['ip']
            region_code = floating_item['region']['slug']
            region = self.env['unison.region']
            region = region.search([('code', '=', region_code)])
            region_id = region.id

            # Check if floating ip is attached to node
            if floating_item['droplet'] == None:
                node_id = None
            else:
                droplet = floating_item['droplet']
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
        for volume_item in volumes:
            code = volume_item['id']
            region_code = volume_item['region']['slug']
            region = self.env['unison.region']
            region = region.search([('code', '=', region_code)])
            region_id = region.id

            # Check if volume is attached to node
            if len(volume_item['droplet_ids']) == 0:
                node_id = None
            else:
                droplet_code = volume_item['droplet_ids'][0]
                node = self.env['unison.node']
                node = node.search([('code', '=', droplet_code)])
                node_id = node.id

            volume = self.env['unison.volume']
            volume = volume.search([('code', '=', code)])
            if len(volume) > 0:
                # Update info about the volume (attach info and size)
                volume.write({
                    'node_id': node_id,
                    'size_gb': volume_item['size_gigabytes']
                })
            else:
                # Create volume
                print "UNISON: Creating volume " + code
                volume = volume.create({
                    'code': code,
                    'name': volume_item['name'],
                    'size_gb': volume_item['size_gigabytes'],
                    'region_id': region_id,
                    'node_id': node_id,
                    'filesystem': None, # Will be provided by UniSon
                    'mount_point': None, # Will be provided by UniSon
                    'notes': '',
                    'active': True
                })

        print "UNISON: Completed hot refresh of clouds"

        return True

    # This function is used to refresh the information about
    # registered repos (branches, modules, etc)
    @api.model
    def repos_refresh(self):
        print "UNISON: Refreshing repositories information"
        home_path = os.getenv("HOME")
        repos_path = home_path + '/repos/'
        if not os.path.isdir(repos_path):
            os.mkdir(repos_path)

        repos = self.env['unison.repo']
        repos = repos.search([])
        for repo in repos:
            group_name = repo.repo_group_id.name
            repo_path = repos_path + group_name + '/' + repo.name
            if not os.path.isdir(repo_path + '/.git'):
                print 'Cloning ' + repo.repo_url() + ' into ' + repo_path

                if repo.clone_command == False:
                    # If no special clone command was configured, clone via https
                    clone_command = "git clone " + repo.repo_url() + ' ' + repo_path
                else:
                    # Otherwise clone the repo using the provided command
                    clone_command = repo.clone_command + ' ' + repo_path

                if repo.is_private:
                    # We should use ssh cloning with the provided key
                    key_path = home_path + '/.ssh/' + group_name + '_' + repo.name
                    file = open(key_path, 'w')
                    file.write(repo.ssh_private_key)
                    clone_command = "export GIT_SSH_COMMAND='ssh -i " + key_path + "'; " + clone_command

                print "Executing " + clone_command
                self.run_command(clone_command)

        # Refreshing branches information
        repos = repos.search([])
        for repo in repos:
            group_name = repo.repo_group_id.name
            repo_path = repos_path + group_name + '/' + repo.name
            command = "cd " + repo_path + " && git branch -r | grep -v HEAD | cut -d '/' -f 2 | tr '\n' ' '"
            output = self.run_command(command)
            branches = output.split(" ")
            for branch_name in branches:
                if len(branch_name) > 0:
                    print "UNISON: Analyzing branch " + group_name + "/" + repo.name + "/" + branch_name + "..."

                    # Change to branch, pull last changes
                    command = "cd " + repo_path + " && git clean -d -fx '' && git checkout " + branch_name + " && git pull origin " + branch_name
                    self.run_command(command)

                    # Get last commit on branch (we use a separate command to not mix the output of other commands)
                    command = "cd " + repo_path + " && git log -1 --pretty=format:%H"
                    last_commit = self.run_command(command)

                    branch = self.env['unison.branch']
                    branch = branch.search([('repo_id', '=', repo.id), ('name', '=', branch_name)])
                    if len(branch) == 0:
                        print "UNISON: Registering branch " + branch_name
                        branch = branch.create({
                            'name': branch_name,
                            'repo_id': repo.id,
                            'last_commit': last_commit,
                        })
                    else:
                        branch.write({
                            'last_commit': last_commit,
                        })

                    # Check the modules included on this branch of the repo
                    # If this repo is a main repo, modules are placed below
                    # of the /addons subdirectory
                    modules_dir = repo_path
                    if branch.repo_id.is_main:
                        modules_dir = modules_dir + "/addons"

                    # Check all the subdirectories (just one sublevel)
                    for dirname in os.listdir(modules_dir):
                        if os.path.isdir(os.path.join(modules_dir, dirname)):
                            module_code = dirname
                            module_path = modules_dir + "/" + module_code
                            # Check if this directory is really a module
                            manifest_file = module_path + "/__openerp__.py"
                            if os.path.isfile(manifest_file):
                                # Get information from Module configuration
                                name = self.get_module_config(manifest_file, 'name');
                                description = self.get_module_config(manifest_file, 'description');
                                summary = self.get_module_config(manifest_file, 'summary');
                                category = self.get_module_config(manifest_file, 'category');
                                version = self.get_module_config(manifest_file, 'version');
                                license = self.get_module_config(manifest_file, 'license');
                                installable = self.get_module_config(manifest_file, 'installable');
                                auto_install = self.get_module_config(manifest_file, 'auto_install');
                                application = self.get_module_config(manifest_file, 'application');
                                author = self.get_module_config(manifest_file, 'author');
                                website = self.get_module_config(manifest_file, 'website');

                                # Check if this module exists
                                module = self.env['unison.module']
                                module = module.search([('branch_id', '=', branch.id), ('code', '=', module_code)])
                                if len(module) == 0:
                                    print "UNISON: Registering module " + module_code + " on branch " + branch_name
                                    module = module.create({
                                        'code': module_code,
                                        'name': name,
                                        'branch_id': branch.id,
                                        'description': description,
                                        'summary': summary,
                                        'category': category,
                                        'version': version,
                                        'license': license,
                                        'installable': installable,
                                        'auto_install': auto_install,
                                        'application': application,
                                        'author': author,
                                        'website': website,
                                    })
                                else:
                                    module.write({
                                        'code': module_code,
                                        'name': name,
                                        'branch_id': branch.id,
                                        'description': description,
                                        'summary': summary,
                                        'category': category,
                                        'version': version,
                                        'license': license,
                                        'installable': installable,
                                        'auto_install': auto_install,
                                        'application': application,
                                        'author': author,
                                        'website': website,
                                    })

        print "UNISON: Completed refresh of repos"

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

    # This function is used to run a shell command and return their output
    def run_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = process.stdout.read()
        return output

    # This function returns some configuration from a module
    def get_module_config(self, manifest_file, config_name):
        # Try to find the config value surrounded by simple quotes
        grep_command = 'grep "\'' + config_name + '\'"'
        command = "cat " + manifest_file + " | " + grep_command + " | cut -d ':' -f 2"
        output = self.run_command(command)
        if len(output) == 0:
            # Try to find the config value surrounded by double quotes
            grep_command = 'grep \'"' + config_name + '"\''
            command = "cat " + manifest_file + " | " + grep_command + " | cut -d ':' -f 2"
            output = self.run_command(command)

        # Remove special characters
        output = output.strip()
        output = output.replace("\n", "")
        output = output.replace("'", "")
        output = output.replace('"', "")
        output = output.replace(",", "")

        return output


