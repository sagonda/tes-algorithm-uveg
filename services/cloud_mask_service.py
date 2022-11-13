from pyhdf.SD import SD, SDC

class cloud_mask_services:

    def __init__(self,f_Myd35_hours, hours_list):

        self.f_Myd35_hours = f_Myd35_hours
        self.hours_list = hours_list
    

    def cloud_mask(self):
        data_Myd35 = [SD(files, SDC.READ) for files in self.f_Myd35_hours[self.hours_list]]
        sds_obj = [file.select('Cloud_Mask') for file in data_Myd35]
        data = [sds_obj[i].get() for i in range(len(sds_obj))]
        maskVals = [data[i][:,:,:] for i in range(len(data))]
        return maskVals