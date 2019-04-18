import os
import csv
import requests

class MobileDeviceDefinitionsDownloader:
    def __init__(self):
        self.iosDevicesURL = "https://gist.githubusercontent.com/binloan/cd2288c8892e29932de1bc27050aecfe/raw/d2a56bff10b93b6e4266cae7c63e331977a85585/Apple_mobile_device_types.txt"
        self.androidDevicesURL = "http://storage.googleapis.com/play_public/supported_devices.csv"

        self.folder = "downloads"
        self.csv = {
            'Device Identifier' : [],
            'Device Name' : [],
            'Device Manufacturer' : [],
            'Bluetooth Version' : []
        }

    def downloadPrepareParseAndExport(self):
        self.download()
        self.prepare()
        self.export()

    def download(self):
        # check if folder exists
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        # download ios device definition file
        r = requests.get(self.iosDevicesURL, allow_redirects=True)
        open('{}/apple.txt'.format('downloads'), 'wb').write(r.content)
        # download android device definition file
        r2 = requests.get(self.androidDevicesURL, allow_redirects=True)
        open('{}/android_orig.txt'.format('downloads'), 'wb').write(r2.content)
        # fix utf-16 encoding for csv
        with open('{}/android_orig.txt'.format('downloads'), 'rb') as source_file:
            with open('{}/android.txt'.format('downloads'), 'w+b') as dest_file:
                contents = source_file.read()
                dest_file.write(contents.decode('utf-16').encode('utf-8'))
        

    def prepare(self):
        # parse ios device csv
        with open('{}/apple.txt'.format('downloads'), mode='r') as ios_csv_file:
            csv_reader = csv.reader(ios_csv_file, delimiter=':')
            for row in csv_reader:
                self.csv['Device Identifier'].append(row[0].strip())
                self.csv['Device Name'].append(row[1].strip())
                self.csv['Device Manufacturer'].append('Apple')
                self.csv['Bluetooth Version'].append(row[2].strip())
        # parse android device csv
        with open('{}/android.txt'.format('downloads'), mode='r') as android_csv_file:
            csv_reader = csv.reader(android_csv_file, delimiter=',')
            row_id = 0
            for row in csv_reader:
                if row_id == 0:
                    row_id += 1
                    continue
                if row == None:
                    continue
                self.csv['Device Identifier'].append(row[3])
                self.csv['Device Name'].append(row[1])
                self.csv['Device Manufacturer'].append(row[0])
                if "Nexus 6P" in row[1]:
                    self.csv['Bluetooth Version'].append("4.2")
                else:
                    self.csv['Bluetooth Version'].append("N/A")
                row_id += 1
    
    def export(self):
        with open('devices.csv', mode='w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            row = 0
            writer.writerow(self.csv.keys())
            for i in range(len(self.csv['Device Identifier'])):
                writer.writerow([self.csv['Device Identifier'][row],self.csv['Device Name'][row],self.csv['Device Manufacturer'][row],self.csv['Bluetooth Version'][row]])
                row += 1