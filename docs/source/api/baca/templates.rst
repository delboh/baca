.. _baca--templates:

templates
=========

.. automodule:: baca.templates

.. currentmodule:: baca.templates

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.templates

.. raw:: html

   <hr/>

.. rubric:: Score templates
   :class: section-header

.. autosummary::
   :nosignatures:

   ~ScoreTemplate
   ~SingleStaffScoreTemplate
   ~StringTrioScoreTemplate
   ~TwoVoiceStaffScoreTemplate
   ~ViolinSoloScoreTemplate

.. autoclass:: ScoreTemplate

   .. autosummary::
      :nosignatures:

      voice_colors

   .. autosummary::
      :nosignatures:

      group_families
      make_music_context
      make_piano_staff
      make_square_staff_group
      make_staff_group

   .. autosummary::
      :nosignatures:

      defaults

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ScoreTemplate.__call__

   .. container:: inherited

      .. automethod:: ScoreTemplate.__copy__

   .. container:: inherited

      .. automethod:: ScoreTemplate.__eq__

   .. container:: inherited

      .. automethod:: ScoreTemplate.__format__

   .. container:: inherited

      .. automethod:: ScoreTemplate.__hash__

   .. container:: inherited

      .. automethod:: ScoreTemplate.__illustrate__

   .. container:: inherited

      .. automethod:: ScoreTemplate.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ScoreTemplate.allows_instrument

   .. container:: inherited

      .. automethod:: ScoreTemplate.allows_part_assignment

   .. container:: inherited

      .. automethod:: ScoreTemplate.attach_defaults

   .. automethod:: ScoreTemplate.group_families

   .. automethod:: ScoreTemplate.make_music_context

   .. automethod:: ScoreTemplate.make_piano_staff

   .. automethod:: ScoreTemplate.make_square_staff_group

   .. automethod:: ScoreTemplate.make_staff_group

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: ScoreTemplate.always_make_global_rests

   .. autoattribute:: ScoreTemplate.defaults

   .. container:: inherited

      .. autoattribute:: ScoreTemplate.do_not_require_margin_markup

   .. container:: inherited

      .. autoattribute:: ScoreTemplate.part_manifest

   .. container:: inherited

      .. autoattribute:: ScoreTemplate.voice_abbreviations

.. autoclass:: SingleStaffScoreTemplate

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SingleStaffScoreTemplate.__call__

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.__copy__

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.__eq__

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.__format__

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.__hash__

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.__illustrate__

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.allows_instrument

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.allows_part_assignment

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.attach_defaults

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.group_families

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.make_music_context

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.make_piano_staff

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.make_square_staff_group

   .. container:: inherited

      .. automethod:: SingleStaffScoreTemplate.make_staff_group

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: SingleStaffScoreTemplate.always_make_global_rests

   .. container:: inherited

      .. autoattribute:: SingleStaffScoreTemplate.defaults

   .. container:: inherited

      .. autoattribute:: SingleStaffScoreTemplate.do_not_require_margin_markup

   .. container:: inherited

      .. autoattribute:: SingleStaffScoreTemplate.part_manifest

   .. container:: inherited

      .. autoattribute:: SingleStaffScoreTemplate.voice_abbreviations

.. autoclass:: StringTrioScoreTemplate

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: StringTrioScoreTemplate.__call__

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.__copy__

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.__eq__

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.__format__

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.__hash__

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.__illustrate__

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.allows_instrument

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.allows_part_assignment

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.attach_defaults

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.group_families

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.make_music_context

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.make_piano_staff

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.make_square_staff_group

   .. container:: inherited

      .. automethod:: StringTrioScoreTemplate.make_staff_group

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: StringTrioScoreTemplate.always_make_global_rests

   .. container:: inherited

      .. autoattribute:: StringTrioScoreTemplate.defaults

   .. container:: inherited

      .. autoattribute:: StringTrioScoreTemplate.do_not_require_margin_markup

   .. container:: inherited

      .. autoattribute:: StringTrioScoreTemplate.part_manifest

   .. container:: inherited

      .. autoattribute:: StringTrioScoreTemplate.voice_abbreviations

.. autoclass:: TwoVoiceStaffScoreTemplate

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: TwoVoiceStaffScoreTemplate.__call__

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.__copy__

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.__eq__

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.__format__

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.__hash__

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.__illustrate__

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.allows_instrument

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.allows_part_assignment

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.attach_defaults

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.group_families

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.make_music_context

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.make_piano_staff

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.make_square_staff_group

   .. container:: inherited

      .. automethod:: TwoVoiceStaffScoreTemplate.make_staff_group

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: TwoVoiceStaffScoreTemplate.always_make_global_rests

   .. container:: inherited

      .. autoattribute:: TwoVoiceStaffScoreTemplate.defaults

   .. container:: inherited

      .. autoattribute:: TwoVoiceStaffScoreTemplate.do_not_require_margin_markup

   .. container:: inherited

      .. autoattribute:: TwoVoiceStaffScoreTemplate.part_manifest

   .. container:: inherited

      .. autoattribute:: TwoVoiceStaffScoreTemplate.voice_abbreviations

.. autoclass:: ViolinSoloScoreTemplate

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: ViolinSoloScoreTemplate.__call__

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.__copy__

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.__eq__

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.__format__

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.__hash__

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.__illustrate__

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.allows_instrument

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.allows_part_assignment

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.attach_defaults

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.group_families

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.make_music_context

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.make_piano_staff

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.make_square_staff_group

   .. container:: inherited

      .. automethod:: ViolinSoloScoreTemplate.make_staff_group

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: ViolinSoloScoreTemplate.always_make_global_rests

   .. container:: inherited

      .. autoattribute:: ViolinSoloScoreTemplate.defaults

   .. container:: inherited

      .. autoattribute:: ViolinSoloScoreTemplate.do_not_require_margin_markup

   .. container:: inherited

      .. autoattribute:: ViolinSoloScoreTemplate.part_manifest

   .. container:: inherited

      .. autoattribute:: ViolinSoloScoreTemplate.voice_abbreviations