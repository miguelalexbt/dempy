
class DempyList(list):

    def by_device(self, device_id : int):
        for i in range(len(self)):
            if self[i].id == device_id:
                return self[i]
        return None

