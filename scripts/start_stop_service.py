class serviceList:
    def __init__(self, portal_URL_home, username, password, server_select, mosaic_dataset_name, log):
        self.services = []
        self.log = log
        self.mosaic_dataset_name = mosaic_dataset_name
        self.service_list = self.SelectServerAndImageService(portal_URL_home, username, password, server_select,
                                                             mosaic_dataset_name)
        for service in self.service_list:
            if self.mosaic_dataset_name in service.properties.serviceName:
                self.services.append(service)

    def StopStartImageService(self, action):
        for service in self.services:
            if action == 'stop':
                service.stop()
                self.log("\n Stopped : {0}".format(service))
            elif action == 'start':
                service.start()
                self.log("\n Started : {0}".format(service))

    def stop(self):
        self.StopStartImageService("stop")

    def start(self):
        self.StopStartImageService("start")

    def SelectServerAndImageService(self, portal_URL_home, username, password, server_select, mosaic_dataset_name):
        gis = GIS(portal_URL_home, username, password)
        gis_server_list = gis.admin.servers.list()
        service_list = []
        for server in gis_server_list:
            if server_select in str(server):
                for service in server.services.list():
                    if mosaic_dataset_name in service.properties.serviceName:
                        service_list.append(service)
        if len(service_list) == 0:
            self.log("\nThere are no image services that match the mosaic dataset {0}".format(mosaic_dataset_name))
        elif len(service_list) >= 1:
            self.log("\nImage service matching mosaic dataset {0} identified: {1}".format(mosaic_dataset_name, service))
        return (service_list)