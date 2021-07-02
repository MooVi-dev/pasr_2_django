import xml.etree.ElementTree as ET

data_to_db = []


class DataToDb:
    def __init__(self):
        self.purchaseNumber = ''
        self.docPublishDate = ''
        self.purchaseObjectInfo = ''
        self.regNum = ''
        self.fullName = ''
        self.maxPrice = 0

    def __str__(self):
        return f'purchaseNumber: {self.purchaseNumber}, docPublishDate: {self.docPublishDate},  \
               purchaseObjectInfo: {self.purchaseObjectInfo}, regNum: {self.regNum},  \
               fullName: {self.fullName}, maxPrice: {self.maxPrice}'


class ParseItem:

    def __init__(self, doc_path):
        self.tree = ET.parse(doc_path)

    def parse(self):
        try:
            xml_type = self.tree.getroot()
            # 'fcsNotificationEF'
            data_item = DataToDb()
            data = xml_type[1]
            for s in data:
                # print(s.tag)
                if 'purchaseResponsible' in s.tag:
                    for org_item in s:
                        # print(org_item.find('responsibleOrg'))
                        if 'responsibleOrg' in org_item.tag:
                            for org_data in org_item:
                                if 'regNum' in org_data.tag:
                                    data_item.regNum = org_data.text
                                elif 'fullName' in org_data.tag:
                                    data_item.fullName = org_data.text
                elif 'purchaseNumber' in s.tag:
                    data_item.purchaseNumber = s.text
                elif 'docPublishDate' in s.tag:
                    data_item.docPublishDate = s.text
                elif 'purchaseObjectInfo' in s.tag:
                    data_item.purchaseObjectInfo = s.text
                elif 'lot' in s.tag:
                    for el_item in s:
                        if 'maxPrice' in el_item.tag:
                            data_item.maxPrice = el_item.text
            data_to_db.append(data_item)
            # print(data_item)
        except Exception as err:
            print(err.args)


def load_file(doc_path):
    # doc_path = 'ЭА_ОЗ=З(Зыков Оружейная палата)_З(Зыков ДомСтрой) +СО (Рыбаков).xml'
    parsing = ParseItem(doc_path)
    parsing.parse()
    return data_to_db


