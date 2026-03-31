current_interface_option = ''
current_interface_object = {}
current_attack_option = ''

scanned_targets = [('10.25.4.1', 'BC:24:11:6C:79:9A', '', None), ('10.25.4.167', 'C4:65:16:B3:A7:F6', '', None), ('10.25.4.169', None, '', None), ('10.25.4.188', '98:E7:F4:03:63:2E', '', None), ('10.25.4.50', '44:A8:42:34:2D:09', '', None), ('10.25.4.89', '24:5E:BE:07:3A:FC', '', None)]
selected_target = {}
selected_target_index = 0

client_details = {
    'os': None,
    'system_name': None,
    'release': None,
    'machine':None,
}