from bpy.props import *
from ...utility import *
from ...nodes.BASE.node_tree import RenderStackNode
from ...ui.icon_utils import RSN_Preview



rsn_icon = RSN_Preview(image='RSN.png', name='rsn_icon')

class RSNodeRenderListNode(RenderStackNode):
    """Render List Node"""
    bl_idname = 'RSNodeRenderListNode'
    bl_label = 'Render List'

    # action after render
    open_dir: BoolProperty(name='Open folder after render', default=True)
    clean_path: BoolProperty(name='Clean filepath after render', default=True)
    render_display_type: EnumProperty(items=[
        ('NONE', 'Keep User Interface', ''),
        ('SCREEN', 'Maximized Area', ''),
        ('AREA', 'Image Editor', ''),
        ('WINDOW', 'New Window', '')],
        default='WINDOW',
        name='Display')

    processor_node: StringProperty(name='Processor', default='')

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")
        self.outputs.new('RSNodeSocketRenderList', 'Processor')
        self.width = 200

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        # call render button when selected

        col = layout.column()
        col.scale_y = 1.75
        sheet = col.operator("rsn.render_button", text=f'Render Confirm',icon_value=rsn_icon.get_image_icon_id())
        sheet.render_list_node_name = self.name
        sheet.open_dir = self.open_dir
        sheet.clean_path = self.clean_path
        sheet.render_display_type = self.render_display_type
        sheet.processor_node = self.processor_node

        layout.separator(factor=0.2)
        col = layout.column(align=0)
        col.prop(context.scene.render, "use_lock_interface")

        layout.separator(factor=0.2)
        col = layout.column(align=0)
        col.prop(self, 'open_dir')
        col.prop(self, 'clean_path')
        col.prop(self, 'render_display_type')

    def update(self):
        self.auto_update_inputs('RSNodeSocketRenderList', "Task")
        try:
            if self.outputs[0].is_linked:
                p_node = self.outputs[0].links[0].to_node
                if p_node: self.processor_node = p_node.name
            else:
                self.processor_node = ''
        except Exception as e:  # This error shows when the dragging the link off viewer node(Works well with knife tool)
            print(e)  # this seems to be a blender error


def register():
    rsn_icon.register()
    bpy.utils.register_class(RSNodeRenderListNode)


def unregister():
    rsn_icon.unregister()
    bpy.utils.unregister_class(RSNodeRenderListNode)
