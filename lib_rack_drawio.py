import xml.etree.ElementTree as ET
import random
import string
from datetime import datetime, timezone

class DrawioRack:
    def __init__(self):
        # 初始化所有属性
        self.page_width = 827  # 页面宽度
        self.page_height = 1169  # 页面高度
        self.rack_margin_top = 21
        self.rack_margin_bottom = 22
        self.rack_unit_height = 15 * 1.3  # 1U高度增加1.3倍
        self.rack_width = 204 * 1.3  # 机柜宽度增加1.3倍
        self.rack_table = {}
        self.device_icon_mapping = {
            "server": "mxgraph.rack.dell.dell_poweredge_2u",
            "router": "mxgraph.rack.hpe_aruba.switches.jl9826a_5412r_92g_poeplus_4sfp_zl2_switch",
        }
        self.current_diagram = None
        self.diagram_count = 0
        
        # 现在可以安全地调用需要这些属性的方法
        self._create_base_element()

    def save_to_file(self, filename="rack_diagram.drawio"):
        tree = ET.ElementTree(self.root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"Draw.io 文件已生成：{filename}")

    def _generate_random_id(self, length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def _create_base_element(self):
        self.root = ET.Element("mxfile")
        self.root.set("host", "lszhang.com")
        now = datetime.now(timezone.utc)
        iso_format = now.replace(microsecond=0).isoformat()
        iso_format_z = iso_format.replace("+00:00", "Z")
        self.root.set("modified", iso_format_z)
        self.root.set("agent", "Python Script")
        self.root.set("version", "26.0.9")
        
        # 创建第一个图表页
        self._create_new_diagram()

    def _create_new_diagram(self):
        self.diagram_count += 1
        # 修改：使用机柜名称作为页面名称
        diagram_name = f"Rack {self.diagram_count}"
        self.current_diagram = ET.SubElement(self.root, "diagram")
        self.current_diagram.set("name", diagram_name)
        self.current_diagram.set("id", f"rack-{self.diagram_count}")

        mx_graph_model = ET.SubElement(self.current_diagram, "mxGraphModel")
        mx_graph_model.set("dx", "1100")
        mx_graph_model.set("dy", "810")
        mx_graph_model.set("grid", "1")
        mx_graph_model.set("gridSize", "5")
        mx_graph_model.set("guides", "1")
        mx_graph_model.set("tooltips", "1")
        mx_graph_model.set("connect", "1")
        mx_graph_model.set("arrows", "1")
        mx_graph_model.set("fold", "1")
        mx_graph_model.set("page", "1")
        mx_graph_model.set("pageScale", "1")
        mx_graph_model.set("pageWidth", "827")
        mx_graph_model.set("pageHeight", "1169")
        mx_graph_model.set("math", "0")
        mx_graph_model.set("shadow", "0")

        self.root_element = ET.SubElement(mx_graph_model, "root")

        id0 = ET.SubElement(self.root_element, "mxCell")
        id0.set("id", "0")

        id1 = ET.SubElement(self.root_element, "mxCell")
        id1.set("id", "1")
        id1.set("parent", "0")

    def create_rack(self, rack_name="Rack", unit_count=42):
        # 为每个机柜创建新的图表页
        self._create_new_diagram()
        
        # 修改：使用机柜名称作为页面名称
        self.current_diagram.set("name", rack_name)
        
        # 计算机柜高度
        rack_height = self.rack_unit_height * unit_count + self.rack_margin_top + self.rack_margin_bottom
        
        # 计算页面中心
        center_x = self.page_width / 2
        center_y = self.page_height / 2
        
        # 每个机柜都居中显示在各自的页面上
        rack_x = center_x - self.rack_width / 2
        rack_y = center_y - rack_height / 2

        random_id = "rack_" + self._generate_random_id()
        self.rack_table[rack_name] = [random_id, unit_count]

        rack = ET.SubElement(self.root_element, "mxCell")
        rack.set("id", random_id)
        rack.set("value", rack_name)

        scale_factor = 1.3
        # 设置机柜名称为32号字
        font_size = 32  
        style = (
            f"strokeColor=#666666;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;"
            f"verticalAlign=top;outlineConnect=0;shadow=0;dashed=0;shape=mxgraph.rackGeneral.rackCabinet3;"
            f"fillColor2=#f4f4f4;container=1;collapsible=0;childLayout=rack;allowGaps=1;marginLeft=33;"
            f"marginRight=9;marginTop={self.rack_margin_top};marginBottom={self.rack_margin_bottom};"
            f"textColor=#666666;numDisp=descend;rackUnitSize={self.rack_unit_height};"
            f"fontSize={font_size};"  # 设置字体大小为32
        )
        rack.set("style", style)
        rack.set("vertex", "1")
        rack.set("parent", "1")

        rack_geometry = ET.SubElement(rack, "mxGeometry")
        rack_geometry.set("x", str(rack_x))
        rack_geometry.set("y", str(rack_y))
        rack_geometry.set("width", str(self.rack_width))
        rack_geometry.set("height", str(rack_height))
        rack_geometry.set("as", "geometry")
        
        # 添加视图中心标记
        self._set_view_center(rack_x, rack_y, self.rack_width, rack_height)

    def _set_view_center(self, x, y, width, height):
        # 添加一个中心点标记，帮助确保视图居中
        center_marker = ET.SubElement(self.root_element, "mxCell")
        center_marker.set("id", "view_center_" + self._generate_random_id())
        center_marker.set("style", "shape=ellipse;fillColor=#ff0000;strokeColor=#ff0000;opacity=0;")
        center_marker.set("vertex", "1")
        center_marker.set("parent", "1")
        
        marker_geometry = ET.SubElement(center_marker, "mxGeometry")
        marker_geometry.set("x", str(x + width/2 - 1))
        marker_geometry.set("y", str(y + height/2 - 1))
        marker_geometry.set("width", "2")
        marker_geometry.set("height", "2")
        marker_geometry.set("as", "geometry")

    def create_device(self, device_name, device_type, rack_name, floor_in_rack, height, ip='', purpose='', status='', other_data=''):
        if rack_name not in self.rack_table:
            self.create_rack(rack_name)
        rack_id = self.rack_table[rack_name][0]

        device_id = f"{device_type}_{self._generate_random_id()}"

        device_object = ET.SubElement(self.root_element, "object")
        device_object.set("id", device_id)
        device_object.set("label", device_name)

        if ip:
            device_object.set("IP", ip)
        if purpose:
            device_object.set("用途", purpose)
        if status:
            device_object.set("状态", status)

        if other_data:
            pairs = other_data.split('|')
            for pair in pairs:
                key, value = pair.split(':')
                key = key.strip()
                value = value.strip()
                device_object.set(key, value)

        device = ET.SubElement(device_object, "mxCell")
        icon_shape = self.device_icon_mapping.get(device_type, "mxgraph.rack.general.1u_rack_server")
        # 设置设备名字体大小为22号
        font_size = 20  
        style = (
            f"strokeColor=#666666;html=1;labelPosition=right;align=left;spacingLeft=15;shadow=0;dashed=0;"
            f"outlineConnect=0;shape={icon_shape};"
            f"fontSize={font_size};"  # 设置字体大小为22
        )
        device.set("style", style)
        device.set("vertex", "1")
        device.set("parent", rack_id)

        device_geometry = ET.SubElement(device, "mxGeometry")
        device_geometry.set("x", "33")
        this_rack_unit_count = self.rack_table[rack_name][1]
        y = self.rack_margin_top + (this_rack_unit_count - floor_in_rack - height + 1) * self.rack_unit_height
        device_geometry.set("y", str(y))
        # 使用机柜内部宽度的99%，解决视觉间隙问题
        device_width = (self.rack_width - 42) * 1  # 调整设备宽度
        device_geometry.set("width", str(device_width))
        device_geometry.set("height", str(height * self.rack_unit_height))
        device_geometry.set("as", "geometry")    
