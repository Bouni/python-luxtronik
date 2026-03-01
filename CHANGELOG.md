# Changelog

All notable changes to this project are documented here.
This changelog follows the "Keep a Changelog" format and Semantic Versioning.

## [Unreleased]

### Added

- Support multiple data fields on one index. [TODO]
- Support an array style access to the data vector fields like
`parameters['ID_Einst_BWS_akt']`. [#221, #233]
- Support unknown codes in SelectionBase. [#197]
- Support smart-home-interface. Luxtronik firmware v3.90.1 or higher
is required for this. See README for further information. [#190]
- Add a command-line-interface (CLI) with the following commands:
`dump`, `dump-cfi`, `dump.shi`, `changes`, `watch-cfi`, `watch-shi`, `discover`

### Changed

- The values to be written are stored directly in the fields instead
of in a separate queue. [#221, #237]
- The field objects now provide `datatype_class` and `datatype_unit`
instead of `measurement_type`

### Removed

- Remove outdated property to access the internal dictionary
like `parameters.parameters`. [TODO]

### Parameters

- Type of `ID_Einst_HzMK1E_akt` (index `14`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_HzMK1ANH_akt` (index `15`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_HzMK1ABS_akt` (index `16`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_LGST_akt` (index `47`) changed
from `Unknown`to `Celsius`
- Type of `ID_Sollwert_TLG_max` (index `84`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_TRBegr_akt` (index `87`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_HRHyst_akt` (index `88`) changed
from `Unknown`to `Kelvin`
- Type of `ID_Einst_TRErhmax_akt` (index `89`) changed
from `Unknown`to `Kelvin`
- Type of `ID_Einst_ZWEFreig_akt` (index `90`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_TAmax_akt` (index `91`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_TAmin_akt` (index `92`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_TWQmin_akt` (index `93`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_THGmax_akt` (index `94`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_TV2VDBW_akt` (index `96`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_Zugangscode` (index `107`) changed
from `Unknown`to `AccessLevel`
- Type of `ID_Einst_TAbsMin_akt` (index `111`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_HzMK2E_akt` (index `141`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_HzMK2ANH_akt` (index `142`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_HzMK2ABS_akt` (index `143`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_SuHkr_akt` (index `222`) changed
from `Unknown`to `TimerProgram`
- Type of `ID_Einst_SuHkrW0_zeit_0_0` (index `223`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrW0_zeit_0_1` (index `224`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrW0_zeit_1_0` (index `225`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrW0_zeit_1_1` (index `226`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrW0_zeit_2_0` (index `227`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrW0_zeit_2_1` (index `228`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkr25_zeit_0_0` (index `229`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkr25_zeit_0_1` (index `230`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkr25_zeit_1_0` (index `231`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkr25_zeit_1_1` (index `232`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkr25_zeit_2_0` (index `233`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkr25_zeit_2_1` (index `234`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkr25_zeit_0_2` (index `235`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkr25_zeit_0_3` (index `236`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkr25_zeit_1_2` (index `237`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkr25_zeit_1_3` (index `238`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkr25_zeit_2_2` (index `239`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkr25_zeit_2_3` (index `240`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_0` (index `241`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_1` (index `242`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_0` (index `243`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_1` (index `244`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_0` (index `245`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_1` (index `246`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_2` (index `247`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_3` (index `248`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_2` (index `249`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_3` (index `250`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_2` (index `251`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_3` (index `252`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_4` (index `253`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_5` (index `254`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_4` (index `255`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_5` (index `256`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_4` (index `257`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_5` (index `258`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_6` (index `259`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_7` (index `260`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_6` (index `261`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_7` (index `262`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_6` (index `263`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_7` (index `264`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_8` (index `265`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_9` (index `266`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_8` (index `267`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_9` (index `268`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_8` (index `269`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_9` (index `270`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_10` (index `271`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_11` (index `272`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_10` (index `273`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_11` (index `274`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_10` (index `275`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_11` (index `276`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_12` (index `277`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_0_13` (index `278`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_12` (index `279`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_1_13` (index `280`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_12` (index `281`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuHkrTG_zeit_2_13` (index `282`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1_akt` (index `283`) changed
from `Unknown`to `TimerProgram`
- Type of `ID_Einst_SuMk1W0_zeit_0_0` (index `284`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1W0_zeit_0_1` (index `285`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1W0_zeit_1_0` (index `286`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1W0_zeit_1_1` (index `287`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1W0_zeit_2_0` (index `288`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1W0_zeit_2_1` (index `289`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk125_zeit_0_0` (index `290`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk125_zeit_0_1` (index `291`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk125_zeit_1_0` (index `292`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk125_zeit_1_1` (index `293`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk125_zeit_2_0` (index `294`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk125_zeit_2_1` (index `295`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk125_zeit_0_2` (index `296`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk125_zeit_0_3` (index `297`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk125_zeit_1_2` (index `298`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk125_zeit_1_3` (index `299`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk125_zeit_2_2` (index `300`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk125_zeit_2_3` (index `301`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_0` (index `302`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_1` (index `303`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_0` (index `304`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_1` (index `305`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_0` (index `306`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_1` (index `307`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_2` (index `308`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_3` (index `309`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_2` (index `310`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_3` (index `311`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_2` (index `312`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_3` (index `313`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_4` (index `314`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_5` (index `315`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_4` (index `316`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_5` (index `317`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_4` (index `318`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_5` (index `319`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_6` (index `320`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_7` (index `321`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_6` (index `322`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_7` (index `323`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_6` (index `324`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_7` (index `325`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_8` (index `326`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_9` (index `327`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_8` (index `328`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_9` (index `329`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_8` (index `330`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_9` (index `331`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_10` (index `332`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_11` (index `333`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_10` (index `334`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_11` (index `335`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_10` (index `336`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_11` (index `337`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_12` (index `338`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_0_13` (index `339`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_12` (index `340`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_1_13` (index `341`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_12` (index `342`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk1TG_zeit_2_13` (index `343`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2_akt2` (index `344`) changed
from `Unknown`to `TimerProgram`
- Type of `ID_Einst_SuMk2Wo_zeit_0_0` (index `345`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Wo_zeit_0_1` (index `346`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Wo_zeit_1_0` (index `347`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Wo_zeit_1_1` (index `348`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Wo_zeit_2_0` (index `349`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Wo_zeit_2_1` (index `350`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk225_zeit_0_0` (index `351`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk225_zeit_0_1` (index `352`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk225_zeit_1_0` (index `353`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk225_zeit_1_1` (index `354`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk225_zeit_2_0` (index `355`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk225_zeit_2_1` (index `356`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk225_zeit_0_2` (index `357`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk225_zeit_0_3` (index `358`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk225_zeit_1_2` (index `359`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk225_zeit_1_3` (index `360`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk225_zeit_2_2` (index `361`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk225_zeit_2_3` (index `362`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_0` (index `363`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_1` (index `364`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_0` (index `365`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_1` (index `366`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_0` (index `367`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_1` (index `368`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_2` (index `369`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_3` (index `370`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_2` (index `371`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_3` (index `372`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_2` (index `373`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_3` (index `374`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_4` (index `375`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_5` (index `376`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_4` (index `377`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_5` (index `378`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_4` (index `379`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_5` (index `380`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_6` (index `381`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_7` (index `382`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_6` (index `383`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_7` (index `384`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_6` (index `385`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_7` (index `386`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_8` (index `387`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_9` (index `388`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_8` (index `389`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_9` (index `390`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_8` (index `391`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_9` (index `392`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_10` (index `393`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_11` (index `394`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_10` (index `395`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_11` (index `396`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_10` (index `397`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_11` (index `398`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_12` (index `399`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_0_13` (index `400`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_12` (index `401`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_1_13` (index `402`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_12` (index `403`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk2Tg_zeit_2_13` (index `404`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SUBW_akt2` (index `405`) changed
from `Unknown`to `TimerProgram`
- Type of `ID_Einst_SuBwWO_zeit_0_0` (index `406`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwWO_zeit_0_1` (index `407`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwWO_zeit_1_0` (index `408`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwWO_zeit_1_1` (index `409`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwWO_zeit_2_0` (index `410`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwWO_zeit_2_1` (index `411`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwWO_zeit_3_0` (index `412`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwWO_zeit_3_1` (index `413`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwWO_zeit_4_0` (index `414`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwWO_zeit_4_1` (index `415`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_0_0` (index `416`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_0_1` (index `417`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_1_0` (index `418`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_1_1` (index `419`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_2_0` (index `420`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_2_1` (index `421`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_3_0` (index `422`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_3_1` (index `423`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_4_0` (index `424`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_4_1` (index `425`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_0_2` (index `426`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_0_3` (index `427`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_1_2` (index `428`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_1_3` (index `429`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_2_2` (index `430`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_2_3` (index `431`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_3_2` (index `432`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_3_3` (index `433`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_4_2` (index `434`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBw25_zeit_4_3` (index `435`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_0` (index `436`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_1` (index `437`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_0` (index `438`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_1` (index `439`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_0` (index `440`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_1` (index `441`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_0` (index `442`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_1` (index `443`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_0` (index `444`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_1` (index `445`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_2` (index `446`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_3` (index `447`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_2` (index `448`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_3` (index `449`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_2` (index `450`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_3` (index `451`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_2` (index `452`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_3` (index `453`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_2` (index `454`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_3` (index `455`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_4` (index `456`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_5` (index `457`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_4` (index `458`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_5` (index `459`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_4` (index `460`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_5` (index `461`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_4` (index `462`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_5` (index `463`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_4` (index `464`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_5` (index `465`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_6` (index `466`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_7` (index `467`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_6` (index `468`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_7` (index `469`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_6` (index `470`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_7` (index `471`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_6` (index `472`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_7` (index `473`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_6` (index `474`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_7` (index `475`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_8` (index `476`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_9` (index `477`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_8` (index `478`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_9` (index `479`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_8` (index `480`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_9` (index `481`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_8` (index `482`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_9` (index `483`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_8` (index `484`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_9` (index `485`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_10` (index `486`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_11` (index `487`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_10` (index `488`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_11` (index `489`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_10` (index `490`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_11` (index `491`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_10` (index `492`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_11` (index `493`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_10` (index `494`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_11` (index `495`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_12` (index `496`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_0_13` (index `497`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_12` (index `498`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_1_13` (index `499`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_12` (index `500`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_2_13` (index `501`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_12` (index `502`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_3_13` (index `503`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_12` (index `504`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuBwTG_zeit_4_13` (index `505`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP_akt` (index `506`) changed
from `Unknown`to `TimerProgram`
- Type of `ID_Einst_SuZIPWo_zeit_0_0` (index `507`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPWo_zeit_0_1` (index `508`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPWo_zeit_1_0` (index `509`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPWo_zeit_1_1` (index `510`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPWo_zeit_2_0` (index `511`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPWo_zeit_2_1` (index `512`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPWo_zeit_3_0` (index `513`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPWo_zeit_3_1` (index `514`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPWo_zeit_4_0` (index `515`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPWo_zeit_4_1` (index `516`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_0_0` (index `517`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_0_1` (index `518`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_1_0` (index `519`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_1_1` (index `520`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_2_0` (index `521`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_2_1` (index `522`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_3_0` (index `523`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_3_1` (index `524`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_4_0` (index `525`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_4_1` (index `526`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_0_2` (index `527`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_0_3` (index `528`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_1_2` (index `529`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_1_3` (index `530`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_2_2` (index `531`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_2_3` (index `532`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_3_2` (index `533`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_3_3` (index `534`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_4_2` (index `535`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIP25_zeit_4_3` (index `536`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_0` (index `537`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_1` (index `538`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_0` (index `539`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_1` (index `540`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_0` (index `541`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_1` (index `542`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_0` (index `543`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_1` (index `544`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_0` (index `545`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_1` (index `546`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_2` (index `547`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_3` (index `548`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_2` (index `549`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_3` (index `550`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_2` (index `551`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_3` (index `552`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_2` (index `553`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_3` (index `554`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_2` (index `555`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_3` (index `556`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_4` (index `557`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_5` (index `558`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_4` (index `559`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_5` (index `560`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_4` (index `561`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_5` (index `562`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_4` (index `563`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_5` (index `564`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_4` (index `565`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_5` (index `566`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_6` (index `567`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_7` (index `568`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_6` (index `569`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_7` (index `570`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_6` (index `571`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_7` (index `572`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_6` (index `573`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_7` (index `574`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_6` (index `575`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_7` (index `576`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_8` (index `577`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_9` (index `578`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_8` (index `579`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_9` (index `580`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_8` (index `581`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_9` (index `582`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_8` (index `583`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_9` (index `584`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_8` (index `585`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_9` (index `586`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_10` (index `587`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_11` (index `588`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_10` (index `589`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_11` (index `590`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_10` (index `591`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_11` (index `592`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_10` (index `593`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_11` (index `594`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_10` (index `595`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_11` (index `596`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_12` (index `597`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_0_13` (index `598`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_12` (index `599`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_1_13` (index `600`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_12` (index `601`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_2_13` (index `602`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_12` (index `603`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_3_13` (index `604`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_12` (index `605`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuZIPTg_zeit_4_13` (index `606`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb_akt` (index `607`) changed
from `Unknown`to `TimerProgram`
- Type of `ID_Einst_SuSwbWo_zeit_0_0` (index `608`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbWo_zeit_0_1` (index `609`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbWo_zeit_1_0` (index `610`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbWo_zeit_1_1` (index `611`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbWo_zeit_2_0` (index `612`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbWo_zeit_2_1` (index `613`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb25_zeit_0_0` (index `614`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb25_zeit_0_1` (index `615`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb25_zeit_1_0` (index `616`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb25_zeit_1_1` (index `617`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb25_zeit_2_0` (index `618`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb25_zeit_2_1` (index `619`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb25_zeit_0_2` (index `620`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb25_zeit_0_3` (index `621`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb25_zeit_1_2` (index `622`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb25_zeit_1_3` (index `623`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb25_zeit_2_2` (index `624`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwb25_zeit_2_3` (index `625`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_0` (index `626`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_1` (index `627`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_0` (index `628`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_1` (index `629`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_0` (index `630`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_1` (index `631`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_2` (index `632`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_3` (index `633`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_2` (index `634`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_3` (index `635`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_2` (index `636`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_3` (index `637`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_4` (index `638`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_5` (index `639`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_4` (index `640`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_5` (index `641`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_4` (index `642`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_5` (index `643`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_6` (index `644`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_7` (index `645`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_6` (index `646`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_7` (index `647`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_6` (index `648`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_7` (index `649`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_8` (index `650`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_9` (index `651`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_8` (index `652`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_9` (index `653`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_8` (index `654`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_9` (index `655`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_10` (index `656`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_11` (index `657`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_10` (index `658`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_11` (index `659`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_10` (index `660`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_11` (index `661`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_12` (index `662`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_0_13` (index `663`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_12` (index `664`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_1_13` (index `665`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_12` (index `666`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuSwbTg_zeit_2_13` (index `667`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Zaehler_BetrZeitWP` (index `668`) changed
from `Unknown`to `Seconds`
- Type of `ID_Zaehler_BetrZeitVD1` (index `669`) changed
from `Unknown`to `Seconds`
- Type of `ID_Zaehler_BetrZeitVD2` (index `670`) changed
from `Unknown`to `Seconds`
- Type of `ID_Zaehler_BetrZeitZWE1` (index `671`) changed
from `Unknown`to `Seconds`
- Type of `ID_Zaehler_BetrZeitZWE2` (index `672`) changed
from `Unknown`to `Seconds`
- Type of `ID_Zaehler_BetrZeitZWE3` (index `673`) changed
from `Unknown`to `Seconds`
- Type of `ID_Zaehler_BetrZeitImpVD1` (index `674`) changed
from `Unknown`to `Count`
- Type of `ID_Zaehler_BetrZeitImpVD2` (index `675`) changed
from `Unknown`to `Count`
- Type of `ID_Ba_Hz_MK1_akt` (index `695`) changed
from `Unknown`to `MixedCircuitMode`
- Type of `ID_Ba_Hz_MK2_akt` (index `696`) changed
from `Unknown`to `MixedCircuitMode`
- Type of `ID_Zaehler_BetrZeitHz` (index `728`) changed
from `Unknown`to `Seconds`
- Type of `ID_Zaehler_BetrZeitBW` (index `729`) changed
from `Unknown`to `Seconds`
- Type of `ID_Zaehler_BetrZeitKue` (index `730`) changed
from `Unknown`to `Seconds`
- Type of `ID_Einst_HzMK3E_akt` (index `774`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_HzMK3ANH_akt` (index `775`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_HzMK3ABS_akt` (index `776`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_SuMk3_akt2` (index `788`) changed
from `Unknown`to `TimerProgram`
- Type of `ID_Einst_SuMk3Wo_zeit_0_0` (index `789`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Wo_zeit_0_1` (index `790`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Wo_zeit_1_0` (index `791`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Wo_zeit_1_1` (index `792`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Wo_zeit_2_0` (index `793`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Wo_zeit_2_1` (index `794`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk325_zeit_0_0` (index `795`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk325_zeit_0_1` (index `796`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk325_zeit_1_0` (index `797`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk325_zeit_1_1` (index `798`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk325_zeit_2_0` (index `799`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk325_zeit_2_1` (index `800`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk325_zeit_0_2` (index `801`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk325_zeit_0_3` (index `802`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk325_zeit_1_2` (index `803`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk325_zeit_1_3` (index `804`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk325_zeit_2_2` (index `805`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk325_zeit_2_3` (index `806`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_0` (index `807`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_1` (index `808`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_0` (index `809`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_1` (index `810`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_0` (index `811`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_1` (index `812`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_2` (index `813`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_3` (index `814`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_2` (index `815`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_3` (index `816`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_2` (index `817`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_3` (index `818`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_4` (index `819`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_5` (index `820`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_4` (index `821`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_5` (index `822`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_4` (index `823`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_5` (index `824`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_6` (index `825`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_7` (index `826`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_6` (index `827`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_7` (index `828`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_6` (index `829`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_7` (index `830`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_8` (index `831`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_9` (index `832`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_8` (index `833`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_9` (index `834`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_8` (index `835`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_9` (index `836`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_10` (index `837`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_11` (index `838`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_10` (index `839`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_11` (index `840`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_10` (index `841`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_11` (index `842`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_12` (index `843`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_0_13` (index `844`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_12` (index `845`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_1_13` (index `846`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_12` (index `847`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Einst_SuMk3Tg_zeit_2_13` (index `848`) changed
from `Unknown`to `TimeOfDay`
- Type of `ID_Waermemenge_Seit` (index `852`) changed
from `Unknown`to `Energy`
- Type of `ID_Waermemenge_Hz` (index `854`) changed
from `Unknown`to `Energy`
- Type of `ID_Zaehler_BetrZeitSW` (index `859`) changed
from `Unknown`to `Seconds`
- Type of `ID_Einst_Popt_Nachlauf_akt` (index `864`) changed
from `Unknown`to `Minutes`
- Type of `ID_Waermemenge_BW` (index `878`) changed
from `Unknown`to `Energy`
- Type of `ID_Waermemenge_SW` (index `879`) changed
from `Unknown`to `Energy`
- Type of `ID_Waermemenge_Datum` (index `880`) changed
from `Unknown`to `Timestamp`
- Type of `ID_Einst_SuLuf_akt` (index `895`) changed
from `Unknown`to `TimerProgram`
- Type of `ID_Einst_SuLufWo_zeit_0_0_0` (index `896`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufWo_zeit_0_1_0` (index `897`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufWo_zeit_0_2_0` (index `898`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLuf25_zeit_0_0_0` (index `899`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLuf25_zeit_0_1_0` (index `900`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLuf25_zeit_0_2_0` (index `901`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLuf25_zeit_0_0_2` (index `902`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLuf25_zeit_0_1_2` (index `903`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLuf25_zeit_0_2_2` (index `904`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_0_0` (index `905`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_1_0` (index `906`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_2_0` (index `907`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_0_2` (index `908`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_1_2` (index `909`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_2_2` (index `910`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_0_4` (index `911`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_1_4` (index `912`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_2_4` (index `913`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_0_6` (index `914`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_1_6` (index `915`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_2_6` (index `916`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_0_8` (index `917`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_1_8` (index `918`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_2_8` (index `919`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_0_10` (index `920`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_1_10` (index `921`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_2_10` (index `922`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_0_12` (index `923`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_1_12` (index `924`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_0_2_12` (index `925`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufWo_zeit_1_0_0` (index `926`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufWo_zeit_1_1_0` (index `927`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufWo_zeit_1_2_0` (index `928`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLuf25_zeit_1_0_0` (index `929`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLuf25_zeit_1_1_0` (index `930`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLuf25_zeit_1_2_0` (index `931`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLuf25_zeit_1_0_2` (index `932`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLuf25_zeit_1_1_2` (index `933`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLuf25_zeit_1_2_2` (index `934`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_0_0` (index `935`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_1_0` (index `936`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_2_0` (index `937`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_0_2` (index `938`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_1_2` (index `939`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_2_2` (index `940`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_0_4` (index `941`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_1_4` (index `942`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_2_4` (index `943`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_0_6` (index `944`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_1_6` (index `945`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_2_6` (index `946`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_0_8` (index `947`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_1_8` (index `948`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_2_8` (index `949`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_0_10` (index `950`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_1_10` (index `951`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_2_10` (index `952`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_0_12` (index `953`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_1_12` (index `954`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_SuLufTg_zeit_1_2_12` (index `955`) changed
from `Unknown`to `TimeOfDay2`
- Type of `ID_Einst_Minimale_Ruecklaufsolltemperatur` (index `979`) changed
from `Unknown`to `Celsius`
- Type of `ID_Einst_Freigabe_Zeit_ZWE` (index `992`) changed
from `Unknown`to `Minutes`
- Type of `ID_Einst_Warmwasser_Nachheizung` (index `994`) changed
from `Unknown`to `Bool`
- Type of `ID_Einst_WW_Nachheizung_max` (index `1020`) changed
from `Unknown`to `Hours2`
- Type of `ID_Waermemenge_ZWE` (index `1059`) changed
from `Unknown`to `Energy`
- Type of `ID_Waermemenge_Reset` (index `1060`) changed
from `Unknown`to `Energy`
- Add `SILENT_MODE` (index `1087`) of type `OnOffMode`
- Add `ID_Einst_SuSilence` (index `1092`) of type `TimerProgram`
- Add `ID_Einst_SilenceTimer_0` (index `1093`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_1` (index `1094`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_2` (index `1095`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_3` (index `1096`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_4` (index `1097`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_5` (index `1098`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_6` (index `1099`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_7` (index `1100`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_8` (index `1101`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_9` (index `1102`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_10` (index `1103`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_11` (index `1104`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_12` (index `1105`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_13` (index `1106`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_14` (index `1107`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_15` (index `1108`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_16` (index `1109`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_17` (index `1110`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_18` (index `1111`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_19` (index `1112`) of type `TimeOfDay2`
- Add `ID_Einst_SilenceTimer_20` (index `1113`) of type `TimeOfDay2`
- Add `LAST_DEFROST_TIMESTAMP` (index `1119`) of type `Timestamp`
- Add `Unknown_Parameter_1126` (index `1126`) of type `Unknown`
- Add `Unknown_Parameter_1127` (index `1127`) of type `Unknown`
- Add `Unknown_Parameter_1128` (index `1128`) of type `Unknown`
- Add `Unknown_Parameter_1129` (index `1129`) of type `Unknown`
- Add `Unknown_Parameter_1130` (index `1130`) of type `Unknown`
- Add `Unknown_Parameter_1131` (index `1131`) of type `Unknown`
- Add `Unknown_Parameter_1132` (index `1132`) of type `Unknown`
- Add `Unknown_Parameter_1133` (index `1133`) of type `Unknown`
- Add `Unknown_Parameter_1134` (index `1134`) of type `Unknown`
- Add `Unknown_Parameter_1135` (index `1135`) of type `Unknown`
- Add `Unknown_Parameter_1136` (index `1136`) of type `Unknown`
- Add `HEAT_ENERGY_INPUT` (index `1136`) of type `Energy`
- Add `Unknown_Parameter_1137` (index `1137`) of type `Unknown`
- Add `DHW_ENERGY_INPUT` (index `1137`) of type `Energy`
- Add `Unknown_Parameter_1138` (index `1138`) of type `Unknown`
- Add `Unknown_Parameter_1139` (index `1139`) of type `Unknown`
- Add `COOLING_ENERGY_INPUT` (index `1139`) of type `Energy`
- Add `Unknown_Parameter_1140` (index `1140`) of type `Unknown`
- Add `SECOND_HEAT_GENERATOR_AMOUNT_COUNTER` (index `1140`) of type `Unknown`
- Add `Unknown_Parameter_1141` (index `1141`) of type `Unknown`
- Add `Unknown_Parameter_1142` (index `1142`) of type `Unknown`
- Add `Unknown_Parameter_1143` (index `1143`) of type `Unknown`
- Add `Unknown_Parameter_1144` (index `1144`) of type `Unknown`
- Add `Unknown_Parameter_1145` (index `1145`) of type `Unknown`
- Add `Unknown_Parameter_1146` (index `1146`) of type `Unknown`
- Add `Unknown_Parameter_1147` (index `1147`) of type `Unknown`
- Add `Unknown_Parameter_1148` (index `1148`) of type `Unknown`
- Add `HEATING_TARGET_TEMP_ROOM_THERMOSTAT` (index `1148`) of type `Celsius`
- Add `Unknown_Parameter_1149` (index `1149`) of type `Unknown`
- Add `Unknown_Parameter_1150` (index `1150`) of type `Unknown`
- Add `Unknown_Parameter_1151` (index `1151`) of type `Unknown`
- Add `Unknown_Parameter_1152` (index `1152`) of type `Unknown`
- Add `Unknown_Parameter_1153` (index `1153`) of type `Unknown`
- Add `Unknown_Parameter_1154` (index `1154`) of type `Unknown`
- Add `Unknown_Parameter_1155` (index `1155`) of type `Unknown`
- Add `Unknown_Parameter_1156` (index `1156`) of type `Unknown`
- Add `Unknown_Parameter_1157` (index `1157`) of type `Unknown`
- Add `Unknown_Parameter_1158` (index `1158`) of type `Unknown`
- Add `POWER_LIMIT_SWITCH` (index `1158`) of type `Unknown`
- Add `Unknown_Parameter_1159` (index `1159`) of type `Unknown`
- Add `POWER_LIMIT_VALUE` (index `1159`) of type `Unknown`

### Calculations

- Type of `ID_WEB_Zaehler_BetrZeitImpVD1` (index `57`) changed
from `Pulses`to `Count`
- Type of `ID_WEB_Zaehler_BetrZeitImpVD2` (index `59`) changed
from `Pulses`to `Count`
- Type of `ID_WEB_AdresseIP_akt` (index `91`) changed
from `IPAddress`to `IPv4Address`
- Type of `ID_WEB_SubNetMask_akt` (index `92`) changed
from `IPAddress`to `IPv4Address`
- Type of `ID_WEB_Add_Broadcast` (index `93`) changed
from `IPAddress`to `IPv4Address`
- Type of `ID_WEB_Add_StdGateway` (index `94`) changed
from `IPAddress`to `IPv4Address`
- Add `ID_WEB_SoftStand_0` (index `81`) of type `Character`
- Add `ID_WEB_SoftStand_1` (index `82`) of type `Character`
- Add `ID_WEB_SoftStand_2` (index `83`) of type `Character`
- Add `ID_WEB_SoftStand_3` (index `84`) of type `Character`
- Add `ID_WEB_SoftStand_4` (index `85`) of type `Character`
- Add `ID_WEB_SoftStand_5` (index `86`) of type `Character`
- Add `ID_WEB_SoftStand_6` (index `87`) of type `Character`
- Add `ID_WEB_SoftStand_7` (index `88`) of type `Character`
- Add `ID_WEB_SoftStand_8` (index `89`) of type `Character`
- Add `ID_WEB_SoftStand_9` (index `90`) of type `Character`
- Add `Vapourisation_Temperature` (index `232`) of type `Celsius`
- Add `Liquefaction_Temperature` (index `233`) of type `Celsius`
- Add `ID_WEB_Freq_VD_Soll` (index `236`) of type `Frequency`
- Add `ID_WEB_Freq_VD_Min` (index `237`) of type `Frequency`
- Add `ID_WEB_Freq_VD_Max` (index `238`) of type `Frequency`
- Add `VBO_Temp_Spread_Soll` (index `239`) of type `Kelvin`
- Add `VBO_Temp_Spread_Ist` (index `240`) of type `Kelvin`
- Add `HUP_PWM` (index `241`) of type `Percent2`
- Add `HUP_Temp_Spread_Soll` (index `242`) of type `Kelvin`
- Add `HUP_Temp_Spread_Ist` (index `243`) of type `Kelvin`
- Add `RBE_Version` (index `258`) of type `MajorMinorVersion`
- Add `Unknown_Calculation_260` (index `260`) of type `Unknown`
- Add `Unknown_Calculation_261` (index `261`) of type `Unknown`
- Add `Unknown_Calculation_262` (index `262`) of type `Unknown`
- Add `Unknown_Calculation_263` (index `263`) of type `Unknown`
- Add `Unknown_Calculation_264` (index `264`) of type `Unknown`
- Add `Unknown_Calculation_265` (index `265`) of type `Unknown`
- Add `Unknown_Calculation_266` (index `266`) of type `Unknown`
- Add `Desired_Room_Temperature` (index `267`) of type `Celsius`
- Add `AC_Power_Input` (index `268`) of type `Power`

### Visibilities

- Add `ID_Visi_Heizung_Zeitschaltprogramm` (index `182`) of type `Unknown`
- Add `Unknown_Visibility_355` (index `355`) of type `Unknown`
- Add `Unknown_Visibility_356` (index `356`) of type `Unknown`
- Add `Unknown_Visibility_357` (index `357`) of type `Unknown`
- Add `ELECTRICAL_POWER_LIMITATION_SWITCH` (index `357`) of type `Unknown`
- Add `Unknown_Visibility_358` (index `358`) of type `Unknown`
- Add `Unknown_Visibility_359` (index `359`) of type `Unknown`
- Add `Unknown_Visibility_360` (index `360`) of type `Unknown`
- Add `Unknown_Visibility_361` (index `361`) of type `Unknown`
- Add `Unknown_Visibility_362` (index `362`) of type `Unknown`
- Add `Unknown_Visibility_363` (index `363`) of type `Unknown`
- Add `Unknown_Visibility_364` (index `364`) of type `Unknown`
- Add `Unknown_Visibility_365` (index `365`) of type `Unknown`
- Add `Unknown_Visibility_366` (index `366`) of type `Unknown`
- Add `Unknown_Visibility_367` (index `367`) of type `Unknown`
- Add `Unknown_Visibility_368` (index `368`) of type `Unknown`
- Add `Unknown_Visibility_369` (index `369`) of type `Unknown`
- Add `Unknown_Visibility_370` (index `370`) of type `Unknown`
- Add `Unknown_Visibility_371` (index `371`) of type `Unknown`
- Add `Unknown_Visibility_372` (index `372`) of type `Unknown`
- Add `Unknown_Visibility_373` (index `373`) of type `Unknown`
- Add `Unknown_Visibility_374` (index `374`) of type `Unknown`
- Add `Unknown_Visibility_375` (index `375`) of type `Unknown`
- Add `Unknown_Visibility_376` (index `376`) of type `Unknown`
- Add `Unknown_Visibility_377` (index `377`) of type `Unknown`
- Add `Unknown_Visibility_378` (index `378`) of type `Unknown`
- Add `Unknown_Visibility_379` (index `379`) of type `Unknown`

## [0.3.14] - 2022-06-07

Last release without a changelog
