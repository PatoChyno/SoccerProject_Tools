from property import Property

PROPERTIES_ORDER = [6, 5, 4, 9, 3, 8, 2, 7, 1]


class Player:

    def __init__(self, player_detail_rows, selected_option, id, name):
        self.properties = {}
        self.selected_option = selected_option
        self.detail_rows = player_detail_rows
        self.id = id
        self.name = name
        self.init_properties()

    def init_properties(self):
        self.extract_properties_from_player_detail()
        self.set_selected_value_from_option()

    def extract_properties_from_player_detail(self):
        row_index = 0
        property_index = 0
        for row in self.detail_rows:
            th_cell = None
            td_index = 0
            for cell in row:
                if cell.name == "th":
                    th_cell = cell
                if cell.name == "td" and (th_cell is not None):
                    if (row_index > 2 and td_index > 0) or td_index > 1:
                        is_property_at_max = cell.has_attr("style")
                        property_name = th_cell.text
                        self.properties[PROPERTIES_ORDER[property_index]] = Property(name=property_name,
                                                                                     value=cell.text.strip(),
                                                                                     is_maxed=is_property_at_max,
                                                                                     is_selected=False,
                                                                                     order=PROPERTIES_ORDER[
                                                                                         property_index])
                        property_index = property_index + 1
                    th_cell = None
                    td_index = td_index + 1
            row_index = row_index + 1

    def set_selected_value_from_option(self):
        if self.selected_option:
            selected_option_value = int(self.selected_option["value"])
            if selected_option_value > 0:
                self.properties[len(PROPERTIES_ORDER) - selected_option_value + 1].is_selected = True

    def selected_property(self):
        for property in self.properties.values():
            if property.is_selected:
                return {
                    "order": property.order,
                    "name": property.name,
                    "is_maxed": property.is_maxed
                }
        return None
