class Properties:
    fileName = 'config.proerties'

    def __init__(self, fileName):
        self.fileName = fileName

    def get_properties(self):

        try:
            pro_file = open(self.fileName, 'r')
            properties = {}
            for line in pro_file:
                if line.find('=') > 0:
                    strs = line.replace('\n', '').split('=')
                    properties[strs[0].strip()] = strs[1]

        except Exception as e:
            raise e
        else:
            pro_file.close()
        return properties


if __name__ == "__main__":
    pro = Properties('config.proerties')
    properties = pro.get_properties()
    print(type(properties))
    print(properties)
    print(properties['input_path'])
