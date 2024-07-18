
def generate_python_file(file_name, data, *imports):
    def dict_to_str(d, indent=0):
        """Converts a dictionary to a string with indentation."""
        lines = []
        indent_str = "    " * indent
        for key, value in d.items():
            if isinstance(value, dict):
                lines.append(f'{indent_str}"{key}" : {{')
                lines.append(dict_to_str(value, indent + 1))
                lines.append(f'{indent_str}}},')
            elif isinstance(value, (tuple, list)):
                lines.append(f'{indent_str}"{key}" : (')
                for item in value:
                    if isinstance(item, dict):
                        lines.append(f'{indent_str}{{')
                        lines.append(dict_to_str(item, indent + 1))
                        lines.append(f'{indent_str}}},')
                    elif isinstance(item, str):
                        lines.append(f'{indent_str + "    "}"{item}",')
                    else:
                        lines.append(f'{indent_str}{item},')
                lines.append(f'{indent_str}),')
            elif isinstance(value, str):
                lines.append(f'{indent_str}"{key}" : "{value}",')
            else:
                lines.append(f'{indent_str}"{key}" : {value},')
        return "\n".join(lines)


    content = "##################################################################################\n### uiscript generated using m2 ui designer by flightm0de @ metin2downloads.to ###\n##################################################################################\n\n\n"
    for import_file in imports:
        content += f"import {import_file}\n"
    content += "\nwindow = {\n"
    content += dict_to_str(data, 1)
    content += "\n}\n"

    with open(file_name, "w") as file:
        file.write(content)

# Example usage
# window_data = {
#     "name": "Acce_CombineWindow",
#     "x": 0,
#     "y": 0,
#     "style": (
#         "movable",
#         "float",
#     ),
#     "width": 215,
#     "height": 270,
#     "children": (
#         {
#             "name": "board",
#             "type": "board",
#             "style": (
#                 "attach",
#             ),
#             "x": 0,
#             "y": 0,
#             "width": 215,
#             "height": 270,
#             "children": (
#                 {
#                     "name": "TitleBar",
#                     "type": "titlebar",
#                     "style": (
#                         "attach",
#                     ),
#                     "x": 6,
#                     "y": 6,
#                     "width": 200,
#                     "color": "yellow",
#                     "children": (
#                         {
#                             "name": "TitleName",
#                             "type": "text",
#                             "x": 95,
#                             "y": 3,
#                             "text": "uiScriptLocale.ACCE_COMBINE",
#                             "text_horizontal_align": "center",
#                         },
#                     ),
#                 },
#                 {
#                     "name": "Acce_Combine",
#                     "type": "image",
#                     "x": 9,
#                     "y": 35,
#                     "image": "acce/acce_combine.tga",
#                     "children": (
#                         {
#                             "name": "AcceSlot",
#                             "type": "slot",
#                             "x": 3,
#                             "y": 3,
#                             "width": 200,
#                             "height": 150,
#                             "slot": (
#                                 {
#                                     "index": 0,
#                                     "x": 78,
#                                     "y": 7,
#                                     "width": 32,
#                                     "height": 32,
#                                 },
#                                 {
#                                     "index": 1,
#                                     "x": 78,
#                                     "y": 60,
#                                     "width": 32,
#                                     "height": 32,
#                                 },
#                                 {
#                                     "index": 2,
#                                     "x": 78,
#                                     "y": 115,
#                                     "width": 32,
#                                     "height": 32,
#                                 },
#                             ),
#                         },
#                         {
#                             "name": "Main",
#                             "type": "text",
#                             "text": "uiScriptLocale.ACCE_MAIN",
#                             "text_horizontal_align": "center",
#                             "x": 97,
#                             "y": 43,
#                         },
#                         {
#                             "name": "serve",
#                             "type": "text",
#                             "text": "uiScriptLocale.ACCE_SERVE",
#                             "text_horizontal_align": "center",
#                             "x": 97,
#                             "y": 98,
#                         },
#                         {
#                             "name": "Result",
#                             "type": "text",
#                             "text": "uiScriptLocale.ACCE_RESULT",
#                             "text_horizontal_align": "center",
#                             "x": 97,
#                             "y": 155,
#                         },
#                     ),
#                 },
#                 {
#                     "name": "NeedMoney",
#                     "type": "text",
#                     "text": "",
#                     "text_horizontal_align": "center",
#                     "x": 105,
#                     "y": 215,
#                 },
#                 {
#                     "name": "AcceptButton",
#                     "type": "button",
#                     "x": 40,
#                     "y": 235,
#                     "text": "uiScriptLocale.OK",
#                     "default_image": "d:/ymir work/ui/public/middle_button_01.sub",
#                     "over_image": "d:/ymir work/ui/public/middle_button_02.sub",
#                     "down_image": "d:/ymir work/ui/public/middle_button_03.sub",
#                 },
#                 {
#                     "name": "CancelButton",
#                     "type": "button",
#                     "x": 114,
#                     "y": 235,
#                     "text": "uiScriptLocale.CANCEL",
#                     "default_image": "d:/ymir work/ui/public/middle_button_01.sub",
#                     "over_image": "d:/ymir work/ui/public/middle_button_02.sub",
#                     "down_image": "d:/ymir work/ui/public/middle_button_03.sub",
#                 },
#             ),
#         },
#     ),
# }

# generate_python_file("acce_combine_window.py", window_data, "uiScriptLocale", "item", "app")
