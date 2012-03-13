from scf.editors.get_dynamic_handler_editor import get_dynamic_handler_editor
from scf.makers.MaterialPackageMaker import MaterialPackageMaker
from scf.wizards.DynamicHandlerCreationWizard import DynamicHandlerCreationWizard
from handlers.dynamics.DynamicHandler import DynamicHandler


class DynamicHandlerMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'dynamic handler'
    output_material_checker = staticmethod(lambda x: isinstance(x, DynamicHandler))
    output_material_editor = staticmethod(get_dynamic_handler_editor)
    output_material_maker = DynamicHandlerCreationWizard 
    output_material_module_import_statements = [
        'from abjad.tools import durationtools',
        'import handlers',
        ] 
