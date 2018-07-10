.. _baca--overrides:

overrides
=========

.. automodule:: baca.overrides

.. currentmodule:: baca.overrides

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.overrides

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~OverrideCommand

.. autoclass:: OverrideCommand

   .. autosummary::
      :nosignatures:

      after
      attribute
      blacklist
      context
      grob
      value
      whitelist

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: OverrideCommand.__call__

   .. container:: inherited

      .. automethod:: OverrideCommand.__format__

   .. container:: inherited

      .. automethod:: OverrideCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: OverrideCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: OverrideCommand.map

   .. container:: inherited

      .. autoattribute:: OverrideCommand.runtime

   .. container:: inherited

      .. autoattribute:: OverrideCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: OverrideCommand.after

   .. autoattribute:: OverrideCommand.attribute

   .. autoattribute:: OverrideCommand.blacklist

   .. autoattribute:: OverrideCommand.context

   .. container:: inherited

      .. autoattribute:: OverrideCommand.deactivate

   .. autoattribute:: OverrideCommand.grob

   .. container:: inherited

      .. autoattribute:: OverrideCommand.measures

   .. container:: inherited

      .. autoattribute:: OverrideCommand.selector

   .. container:: inherited

      .. autoattribute:: OverrideCommand.tag

   .. container:: inherited

      .. autoattribute:: OverrideCommand.tags

   .. autoattribute:: OverrideCommand.value

   .. autoattribute:: OverrideCommand.whitelist

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~accidental_stencil_false
   ~accidental_transparent
   ~accidental_x_extent_false
   ~bar_extent
   ~bar_extent_zero
   ~bar_line_transparent
   ~beam_positions
   ~beam_stencil_false
   ~beam_transparent
   ~clef_extra_offset
   ~clef_shift
   ~clef_x_extent_false
   ~dls_padding
   ~dls_staff_padding
   ~dls_up
   ~dots_stencil_false
   ~dots_transparent
   ~dynamic_shift
   ~dynamic_text_center
   ~dynamic_text_extra_offset
   ~dynamic_text_left
   ~dynamic_text_parent_alignment_x
   ~dynamic_text_right
   ~dynamic_text_stencil_false
   ~dynamic_text_transparent
   ~dynamic_text_x_extent_zero
   ~dynamic_text_x_offset
   ~dynamic_text_y_offset
   ~flag_stencil_false
   ~flag_transparent
   ~glissando_thickness
   ~hairpin_shorten_pair
   ~hairpin_start_shift
   ~hairpin_stencil_false
   ~hairpin_transparent
   ~mmrest_text_color
   ~mmrest_text_extra_offset
   ~mmrest_text_padding
   ~mmrest_text_parent_center
   ~mmrest_text_staff_padding
   ~no_ledgers
   ~note_column_shift
   ~note_head_color
   ~note_head_stencil_false
   ~note_head_style_cross
   ~note_head_style_harmonic
   ~note_head_transparent
   ~ottava_bracket_staff_padding
   ~rehearsal_mark_extra_offset
   ~rehearsal_mark_y_offset
   ~repeat_tie_down
   ~repeat_tie_stencil_false
   ~repeat_tie_transparent
   ~repeat_tie_up
   ~rest_down
   ~rest_extra_offset
   ~rest_position
   ~rest_transparent
   ~rest_up
   ~script_color
   ~script_down
   ~script_extra_offset
   ~script_padding
   ~script_staff_padding
   ~script_up
   ~slur_down
   ~slur_up
   ~span_bar_color
   ~span_bar_extra_offset
   ~span_bar_transparent
   ~stem_color
   ~stem_down
   ~stem_stencil_false
   ~stem_transparent
   ~stem_up
   ~strict_note_spacing_off
   ~sustain_pedal_staff_padding
   ~text_script_color
   ~text_script_down
   ~text_script_extra_offset
   ~text_script_font_size
   ~text_script_padding
   ~text_script_parent_center
   ~text_script_staff_padding
   ~text_script_up
   ~text_script_x_offset
   ~text_script_y_offset
   ~text_spanner_left_padding
   ~text_spanner_right_padding
   ~text_spanner_staff_padding
   ~text_spanner_stencil_false
   ~text_spanner_transparent
   ~text_spanner_y_offset
   ~tie_down
   ~tie_up
   ~time_signature_extra_offset
   ~time_signature_transparent
   ~tremolo_down
   ~trill_spanner_staff_padding
   ~tuplet_bracket_down
   ~tuplet_bracket_extra_offset
   ~tuplet_bracket_outside_staff_priority
   ~tuplet_bracket_padding
   ~tuplet_bracket_shorten_pair
   ~tuplet_bracket_staff_padding
   ~tuplet_bracket_up
   ~tuplet_number_denominator
   ~tuplet_number_extra_offset

.. autofunction:: accidental_stencil_false

.. autofunction:: accidental_transparent

.. autofunction:: accidental_x_extent_false

.. autofunction:: bar_extent

.. autofunction:: bar_extent_zero

.. autofunction:: bar_line_transparent

.. autofunction:: beam_positions

.. autofunction:: beam_stencil_false

.. autofunction:: beam_transparent

.. autofunction:: clef_extra_offset

.. autofunction:: clef_shift

.. autofunction:: clef_x_extent_false

.. autofunction:: dls_padding

.. autofunction:: dls_staff_padding

.. autofunction:: dls_up

.. autofunction:: dots_stencil_false

.. autofunction:: dots_transparent

.. autofunction:: dynamic_shift

.. autofunction:: dynamic_text_center

.. autofunction:: dynamic_text_extra_offset

.. autofunction:: dynamic_text_left

.. autofunction:: dynamic_text_parent_alignment_x

.. autofunction:: dynamic_text_right

.. autofunction:: dynamic_text_stencil_false

.. autofunction:: dynamic_text_transparent

.. autofunction:: dynamic_text_x_extent_zero

.. autofunction:: dynamic_text_x_offset

.. autofunction:: dynamic_text_y_offset

.. autofunction:: flag_stencil_false

.. autofunction:: flag_transparent

.. autofunction:: glissando_thickness

.. autofunction:: hairpin_shorten_pair

.. autofunction:: hairpin_start_shift

.. autofunction:: hairpin_stencil_false

.. autofunction:: hairpin_transparent

.. autofunction:: mmrest_text_color

.. autofunction:: mmrest_text_extra_offset

.. autofunction:: mmrest_text_padding

.. autofunction:: mmrest_text_parent_center

.. autofunction:: mmrest_text_staff_padding

.. autofunction:: no_ledgers

.. autofunction:: note_column_shift

.. autofunction:: note_head_color

.. autofunction:: note_head_stencil_false

.. autofunction:: note_head_style_cross

.. autofunction:: note_head_style_harmonic

.. autofunction:: note_head_transparent

.. autofunction:: ottava_bracket_staff_padding

.. autofunction:: rehearsal_mark_extra_offset

.. autofunction:: rehearsal_mark_y_offset

.. autofunction:: repeat_tie_down

.. autofunction:: repeat_tie_stencil_false

.. autofunction:: repeat_tie_transparent

.. autofunction:: repeat_tie_up

.. autofunction:: rest_down

.. autofunction:: rest_extra_offset

.. autofunction:: rest_position

.. autofunction:: rest_transparent

.. autofunction:: rest_up

.. autofunction:: script_color

.. autofunction:: script_down

.. autofunction:: script_extra_offset

.. autofunction:: script_padding

.. autofunction:: script_staff_padding

.. autofunction:: script_up

.. autofunction:: slur_down

.. autofunction:: slur_up

.. autofunction:: span_bar_color

.. autofunction:: span_bar_extra_offset

.. autofunction:: span_bar_transparent

.. autofunction:: stem_color

.. autofunction:: stem_down

.. autofunction:: stem_stencil_false

.. autofunction:: stem_transparent

.. autofunction:: stem_up

.. autofunction:: strict_note_spacing_off

.. autofunction:: sustain_pedal_staff_padding

.. autofunction:: text_script_color

.. autofunction:: text_script_down

.. autofunction:: text_script_extra_offset

.. autofunction:: text_script_font_size

.. autofunction:: text_script_padding

.. autofunction:: text_script_parent_center

.. autofunction:: text_script_staff_padding

.. autofunction:: text_script_up

.. autofunction:: text_script_x_offset

.. autofunction:: text_script_y_offset

.. autofunction:: text_spanner_left_padding

.. autofunction:: text_spanner_right_padding

.. autofunction:: text_spanner_staff_padding

.. autofunction:: text_spanner_stencil_false

.. autofunction:: text_spanner_transparent

.. autofunction:: text_spanner_y_offset

.. autofunction:: tie_down

.. autofunction:: tie_up

.. autofunction:: time_signature_extra_offset

.. autofunction:: time_signature_transparent

.. autofunction:: tremolo_down

.. autofunction:: trill_spanner_staff_padding

.. autofunction:: tuplet_bracket_down

.. autofunction:: tuplet_bracket_extra_offset

.. autofunction:: tuplet_bracket_outside_staff_priority

.. autofunction:: tuplet_bracket_padding

.. autofunction:: tuplet_bracket_shorten_pair

.. autofunction:: tuplet_bracket_staff_padding

.. autofunction:: tuplet_bracket_up

.. autofunction:: tuplet_number_denominator

.. autofunction:: tuplet_number_extra_offset