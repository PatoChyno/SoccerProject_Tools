class Property:

    def __init__(self, name, value=0, is_maxed=False, is_selected=False, order=0):
        self.name = name
        self.value = int(value[:-1])
        self.is_maxed = is_maxed
        self.is_selected = is_selected
        self.order: int = order
        self.is_stamina = (order == 9)
