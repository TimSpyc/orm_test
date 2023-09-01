if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from backend.models.reference_models import *
from datetime import date

fake = Faker()

def createCurrencies():
    currency = Currency(
        name = 'euro',
        abbreviation = 'eur',
        symbol = '€'
    )
    currency.save()

    currency = Currency(
        name = 'us-dollar',
        abbreviation = 'usd',
        symbol = '$'
    )
    currency.save()

    currency = Currency(
        name = 'pound',
        abbreviation = 'gbp',
        symbol = '£'
    )
    currency.save()

    currency = Currency(
        name = 'franc',
        abbreviation = 'chf',
        symbol = 'CHF'
    )
    currency.save()

def createNormTypes():
    norm_type = NormType(
        name = 'material'
    )
    norm_type.save()

    norm_type = NormType(
        name = 'part'
    )
    norm_type.save()

    norm_type = NormType(
        name = 'other'
    )
    norm_type.save()

def createPartTypes():
    part_type_list = [
        {"name_csg":"adapter"},
        {"name_csg":"adhesive"},
        {"name_csg":"assembly"},
        {"name_csg":"barrier"},
        {"name_csg":"baseplate"},
        {"name_csg":"battery"},
        {"name_csg":"battery enclosure"},
        {"name_csg":"bearing"},
        {"name_csg":"blind rivet"},
        {"name_csg":"blind rivet nut"},
        {"name_csg":"blind rivet stud"},
        {"name_csg":"bolt"},
        {"name_csg":"bushing"},
        {"name_csg":"cage nut"},
        {"name_csg":"camera protection"},
        {"name_csg":"crash can"},
        {"name_csg":"crash management system"},
        {"name_csg":"cross member"},
        {"name_csg":"door"},
        {"name_csg":"fascia"},
        {"name_csg":"foam"},
        {"name_csg":"frame"},
        {"name_csg":"heat sink"},
        {"name_csg":"holder"},
        {"name_csg":"joining definition"},
        {"name_csg":"locator definition"},
        {"name_csg":"longitudinal member"},
        {"name_csg":"measuring point"},
        {"name_csg":"member"},
        {"name_csg":"misc."},
        {"name_csg":"node"},
        {"name_csg":"nut"},
        {"name_csg":"nut plate"},
        {"name_csg":"package"},
        {"name_csg":"pillar"},
        {"name_csg":"pin"},
        {"name_csg":"plate"},
        {"name_csg":"press nut"},
        {"name_csg":"press stud"},
        {"name_csg":"profile"},
        {"name_csg":"punch nut"},
        {"name_csg":"reinforcement"},
        {"name_csg":"rivet"},
        {"name_csg":"seal"},
        {"name_csg":"seat cross member"},
        {"name_csg":"shaft"},
        {"name_csg":"sheet"},
        {"name_csg":"side impact beam"},
        {"name_csg":"sill"},
        {"name_csg":"spacer"},
        {"name_csg":"speed nut"},
        {"name_csg":"stopper"},
        {"name_csg":"strut"},
        {"name_csg":"sub-assembly"},
        {"name_csg":"sub-frame"},
        {"name_csg":"support"},
        {"name_csg":"surface treatment"},
        {"name_csg":"suspension part"},
        {"name_csg":"threaded insert"},
        {"name_csg":"towing eye mount"},
        {"name_csg":"towing hook"},
        {"name_csg":"tunnel"},
        {"name_csg":"wall"},
        {"name_csg":"washer"},
        {"name_csg":"welding nut"},
        {"name_csg":"welding seam"},
        {"name_csg":"welding spot"},
        {"name_csg":"welding stud"},
        {"name_csg":"wheel claw"}
    ]
    for part_type in part_type_list:
        part_type = PartType(
            name = part_type['name_csg']
        )
        part_type.save()

def createPartPositions():
    part_position_list = [
        '1lp',
        '2lp',
        '3lp',
        'front',
        'rear',
        'inner',
        'outer',
        'left',
        'right',
        'center',
    ]
    for part_position in part_position_list:
        part_position = PartPosition(
            name = part_position
        )
        part_position.save()

def createSemiFinishedProductTypes():
    semi_finished_product_type_list = [
        'profile',
        'standard_part',
        'sheet metal part - steel'
        'sheet metal part - aluminium',
        'cast part',
        'forged part',
        'plastic part',
    ]
    for semi_finished_product_type in semi_finished_product_type_list:
        semi_finished_product_type = SemiFinishedProductType(
            name = semi_finished_product_type
        )
        semi_finished_product_type.save()

def createMaterialTypes():
    material_type_list = [
        'aluminum',
        'steel',
        'polymer',
        'iron'
        'other',
    ]
    for material_type in material_type_list:
        material_type = MaterialType(
            name = material_type
        )
        material_type.save()
    
def createPartSoldPriceComponentTypes():
    part_sold_price_component_type_list = [
        'value add',
        'additional logistic',
        'material overhead',
        'energy',
        'path through',
        'product development allocation',
        'call off change',
        'spare part',
        'other',
    ]

    for part_sold_price_component_type in part_sold_price_component_type_list:
        part_sold_price_component_type = PartSoldPriceComponentType(
            name = part_sold_price_component_type
        )
        part_sold_price_component_type.save()

def createPriceUploadSources():
    price_upload_source_list = [
        'customer',
        'internal',
        'other',
    ]

    for price_upload_source in price_upload_source_list:
        price_upload_source = PriceUploadSource(
            name = price_upload_source
        )
        price_upload_source.save()

def createSavingUnits():
    saving_unit_list = [
        'currency',
        'percent',
    ]

    for saving_unit in saving_unit_list:
        saving_unit = SavingUnit(
            name = saving_unit
        )
        saving_unit.save()

def createPartSoldMaterialPriceTypes():
    part_sold_material_type_list = [
        'lme',
        'ecdp',
        'billet up charge',
        'steel',
    ]

    for part_sold_material_type in part_sold_material_type_list:
        part_sold_material_type = PartSoldMaterialPriceType(
            name = part_sold_material_type
        )
        part_sold_material_type.save()

def createDerivativeTypes():
    derivative_type_list = [
        'crash box front',
        'crash box rear',
        'crash management system front',
        'crash management system rear',
        'bumper front',
        'bumper rear',
        'side impact beam',
        'sill',
        'cross member',
        'strut',
        'body in white',
        'battery box'
    ]

    for derivative_type in derivative_type_list:
        derivative_type = DerivativeType(
            name = derivative_type
        )
        derivative_type.save()

def createPredictionAccuracies():
    prediction_accuracy_list = [
        'low (0-50%)',
        'medium (50-80%)',
        'high (80-100%)',
    ]

    for prediction_accuracy in prediction_accuracy_list:
        prediction_accuracy = PredictionAccuracy(
            name = prediction_accuracy
        )
        prediction_accuracy.save()

def createProjectUserRoles():
    project_user_role_list = [
        'program management',
        'product development',
        'sales',
        'profile procurement',
        'standard part procurement',
        'purchased part procurement',
        'process development',
        'quality',
        'logistic',
        'member'
    ]

    for project_user_role in project_user_role_list:
        project_user_role = ProjectUserRole(
            name = project_user_role
        )
        project_user_role.save()

def createFakeRevisionsLmc(start_year, end_year):
    for year in range(start_year, end_year+1):
        for month in range(1,13):
            lmc_rev = date(year, month, 1)
            RevisionLMC(revision_date = lmc_rev).save()

def createProjectStaffCostTasks():
    project_staff_cost_task_dict = {
        'development': {'description': 'Development', 'psp_element': '010'},
        'simulation': {'description': 'Simulation', 'psp_element': '020'},
        'change management': {'description': 'Change Management', 'psp_element': '030'},
        'research': {'description': 'Research', 'psp_element': '010'},
        'organization': {'description': 'Organization', 'psp_element': '010'},
        'other': {'description': 'Other work that does not fit inside the rest', 'psp_element': '010'},
    }

    for key, value in project_staff_cost_task_dict.items():
        project_staff_cost_task = ProjectStaffCostTask(
            name = key,
            description = value['description'],
            psp_element = value['psp_element']
        )
        project_staff_cost_task.save()

def createAutomatedExecutionInterval():

    interval = log_AutomatedExecutionInterval(
        name = 'daily',
        interval_seconds = 86400,
        description = 'this script is run at least once a day'
    )
    interval.save()

    interval = log_AutomatedExecutionInterval(
        name = 'weekly',
        interval_seconds = 604800,
        description = 'this script is run at least once a week'
    )
    interval.save()

    interval = log_AutomatedExecutionInterval(
        name = 'monthly',
        interval_seconds = 2592000,
        description = 'this script is run at least once a month'
    )
    interval.save()

def createChangeRequestCostCategory():
    cost_category_list = [
        "production line",
        "tooling",
        "jig",
        "gauge",
        "transport container",
        "scrapping old stock",
        "supplier",
        "other"
    ]
    for cost_category in cost_category_list:
        cost_category = ChangeRequestCostCategory(
            name = cost_category
        )
        cost_category.save()

def createChangeRequestRiskCategory():
    risk_category_list = [
        'deadline cannot be met',
        'component does not fulfill its function',
        'component production not stable',
        'costs higher than expected',
        'incorrect installation possible',
        'other'
    ]

    for risk_category in risk_category_list:
        risk_category = ChangeRequestRiskCategory(
            name = risk_category
        )
        risk_category.save()

def createChangeRequestRiskImpact():
    risk_impact_list = [
        {'name': 'no impact', 'factor': 0},
        {'name': 'low', 'factor': 1},
        {'name': 'medium', 'factor': 2},
        {'name': 'high', 'factor': 3},

    ]

    for risk_impact in risk_impact_list:
        risk_impact = ChangeRequestRiskImpact(
            **risk_impact
        )
        risk_impact.save()

def createChangeRequestRiskProbability():
    risk_probability_list = [
        {'name': 'extremely unlikely', 'factor': 0},
        {'name': 'unlikely', 'factor': 1},
        {'name': 'hard to evaluate', 'factor': 2},
        {'name': 'likely', 'factor': 3},
        {'name': 'high probability', 'factor': 5},
    ]

    for risk_probability in risk_probability_list:
        risk_probability = ChangeRequestRiskProbability(
            **risk_probability
        )
        risk_probability.save()

def createFileExtensions():
    file_extension_list = [
        "jpg",
        "jpeg",
        "png",
        "svg",
        "gif",
        "xlsx",
        "xls",
        "csv",
        "docx",
        "doc",
        "pptx",
        "ppt",
        "pdf",
        "txt",
    ]

    for file_extension in file_extension_list:
        file_extension = FileExtension(
            name = file_extension
        )
        file_extension.save()

def createFileTypes():
    file_type_list = [
        {'name': 'image', 'file_extension': ['jpg', 'jpeg', 'png', 'svg', 'gif']},
        {'name': 'excel', 'file_extension': ['xlsx', 'xls', 'csv']},
        {'name': 'word', 'file_extension': ['docx', 'doc']},
        {'name': 'powerpoint', 'file_extension': ['pptx', 'ppt']},
        {'name': 'pdf', 'file_extension': ['pdf']},
        {'name': 'text', 'file_extension': ['txt']},
    ]

    for file_type_dict in file_type_list:
        file_type = FileType(
            name = file_type_dict['name']
        )
        file_type.save()
        for file_extension in file_type_dict['file_extension']:
            file_type.file_extension.add(FileExtension.objects.get(name=file_extension))
        file_type.save()

def createPartReleaseStatus():
    part_release_status_list = [
        {
            'name':'released',
            'description': 'The part is released; all needed signatures are done.',
            'release_hierarchy': 3
        },
        {
            'name':'work status',
            'description': 'The part is currently under design. Only the development engineer works with this part; nobody else.',
            'release_hierarchy': 3
        },
        {
            'name':'withdrawn',
            'description': 'The part was revised and is not used anymore anywhere.',
            'release_hierarchy': 3
        },
        {
            'name':'construction release',
            'description': 'Development Engineer releases the part, but nobody else has signed yet. This state can be used to make first requests for proposals but must not be seen as a freezed design.',
            'release_hierarchy': 3
        },
    ]

    for part_release_status in part_release_status_list:
        part_release_status = PartReleaseStatus(
            **part_release_status
        )
        part_release_status.save()

def createProjectStatus():
    project_status_list = [
        'nomination',
        'series',
        'acquisition',
        'pre development',
        'internal',
        'lost',
    ]

    for project_status in project_status_list:
        project_status = ProjectStatus(
            name = project_status
        )
        project_status.save()

def createProjectType():
    project_type_list = [
        'sustaining',
        'growth',
        'existing'
    ]

    for project_type in project_type_list:
        project_type = ProjectType(
            name = project_type
        )
        project_type.save()

def createTechnology():
    technology_list = [
        'stamping',
        'cnc milling',
        'bending',
        'stretch bending',
        'industrialization',
        'tool construction',
        'milling tool selling',
        'sps programming',
        'electrical engineering',
        'hydro forming',
        'friction stir welding',
        'welding',
        'robot programming',
        'testing',
        'automation standard element selling',
        'sawing',
        'process monitoring',
        'roll bending',
        'hydraulic pressing',
        'hydraulic press tooling',
        'extruding',
        'embossing',
        'washing',
        'sheet metal forming',
        'coating',
        'standard element selling',
        'die casting',
        'forging',
        'plastic injection molding',
        'measuring',
        'assembling',
        'debarring',
        'labeling',
        'melting',
        'casting',
        'heat treading',
        'laser cutting',
        'lathe shaping',
        'grinding',
        'prototyping',
        'bonding',
        'hot forming',
        'miter cutting',
        'part processing',
        'calibrating'
    ]

    for technology in technology_list:
        technology = Technology(
            name = technology
        )
        technology.save()

def createSapAbbreviationDictionary():
    sap_abbreviation_dictionary_list = [
        {"id":"1","sap_abbreviation":"MANDT","description":"Mandant"},
        {"id":"2","sap_abbreviation":"VBELN","description":"Verkaufsbeleg"},
        {"id":"3","sap_abbreviation":"ERDAT","description":"Angelegt am"},
        {"id":"4","sap_abbreviation":"ERZET","description":"Uhrzeit"},
        {"id":"5","sap_abbreviation":"ERNAM","description":"Angelegt von"},
        {"id":"6","sap_abbreviation":"ANGDT","description":"Angebot gültig von"},
        {"id":"7","sap_abbreviation":"BNDDT","description":"Angebot gültig bis"},
        {"id":"8","sap_abbreviation":"AUDAT","description":"Belegdatum"},
        {"id":"9","sap_abbreviation":"VBTYP","description":"Vertriebsbelegtyp"},
        {"id":"10","sap_abbreviation":"TRVOG","description":"Gr.Transakt.Vorgang"},
        {"id":"11","sap_abbreviation":"AUART","description":"Verkaufsbelegart"},
        {"id":"12","sap_abbreviation":"AUGRU","description":"Auftragsgrund"},
        {"id":"13","sap_abbreviation":"GWLDT","description":"Gewährleistung"},
        {"id":"14","sap_abbreviation":"SUBMI","description":"Submission"},
        {"id":"15","sap_abbreviation":"LIFSK","description":"Liefersperre"},
        {"id":"16","sap_abbreviation":"FAKSK","description":"Fakturasperre"},
        {"id":"17","sap_abbreviation":"NETWR","description":"Nettowert"},
        {"id":"18","sap_abbreviation":"WAERK","description":"Belegwährung"},
        {"id":"19","sap_abbreviation":"VKORG","description":"Verkaufsorganisation"},
        {"id":"20","sap_abbreviation":"VTWEG","description":"Vertriebsweg"},
        {"id":"21","sap_abbreviation":"SPART","description":"Sparte"},
        {"id":"22","sap_abbreviation":"VKGRP","description":"Verkäufergruppe"},
        {"id":"23","sap_abbreviation":"VKBUR","description":"Verkaufsbüro"},
        {"id":"24","sap_abbreviation":"GSBER","description":"Geschäftsbereich"},
        {"id":"25","sap_abbreviation":"GSKST","description":"Geschäftsbereich"},
        {"id":"26","sap_abbreviation":"GUEBG","description":"Gültigkeitsbeginn"},
        {"id":"27","sap_abbreviation":"GUEEN","description":"Gültigkeitsende"},
        {"id":"28","sap_abbreviation":"KNUMV","description":"Nr. Belegkondition"},
        {"id":"29","sap_abbreviation":"VDATU","description":"Wunschlieferdatum"},
        {"id":"30","sap_abbreviation":"VPRGR","description":"Periode zum Termin"},
        {"id":"31","sap_abbreviation":"AUTLF","description":"Komplettlieferung"},
        {"id":"32","sap_abbreviation":"VBKLA","description":"Ursprungsssystem"},
        {"id":"33","sap_abbreviation":"VBKLT","description":"Kennzeichnung"},
        {"id":"34","sap_abbreviation":"KALSM","description":"Kalkulationsschema"},
        {"id":"35","sap_abbreviation":"VSBED","description":"Versandbedingung"},
        {"id":"36","sap_abbreviation":"FKARA","description":"Auftr.bez. Fakt.Art"},
        {"id":"37","sap_abbreviation":"AWAHR","description":"Wahrscheinlichkeit"},
        {"id":"38","sap_abbreviation":"KTEXT","description":"Bezeichnung"},
        {"id":"39","sap_abbreviation":"BSTNK","description":"Bestellnummer"},
        {"id":"40","sap_abbreviation":"BSARK","description":"Bestellart"},
        {"id":"41","sap_abbreviation":"BSTDK","description":"Bestelldatum"},
        {"id":"42","sap_abbreviation":"BSTZD","description":"Zusatz"},
        {"id":"43","sap_abbreviation":"IHREZ","description":"Ihr Zeichen"},
        {"id":"44","sap_abbreviation":"BNAME","description":"Name"},
        {"id":"45","sap_abbreviation":"TELF1","description":"Telefon"},
        {"id":"46","sap_abbreviation":"MAHZA","description":"Anzahl Mahnungen"},
        {"id":"47","sap_abbreviation":"MAHDT","description":"Letzte Mahnung"},
        {"id":"48","sap_abbreviation":"KUNNR","description":"Auftraggeber"},
        {"id":"49","sap_abbreviation":"KOSTL","description":"Kostenstelle"},
        {"id":"50","sap_abbreviation":"STAFO","description":"FortschreibGruppe"},
        {"id":"51","sap_abbreviation":"STWAE","description":"Statistikwährung"},
        {"id":"52","sap_abbreviation":"AEDAT","description":"Geändert am"},
        {"id":"53","sap_abbreviation":"KVGR1","description":"Kundengruppe 1"},
        {"id":"54","sap_abbreviation":"KVGR2","description":"Kundengruppe 2"},
        {"id":"55","sap_abbreviation":"KVGR3","description":"Kundengruppe 3"},
        {"id":"56","sap_abbreviation":"KVGR4","description":"Kundengruppe 4"},
        {"id":"57","sap_abbreviation":"KVGR5","description":"Kundengruppe 5"},
        {"id":"58","sap_abbreviation":"KNUMA","description":"Absprache"},
        {"id":"59","sap_abbreviation":"KOKRS","description":"Kostenrechnungskreis"},
        {"id":"60","sap_abbreviation":"PS_PSP_PNR","description":"PSP-Element"},
        {"id":"61","sap_abbreviation":"KURST","description":"Kurstyp"},
        {"id":"62","sap_abbreviation":"KKBER","description":"Kreditkontr.Bereich"},
        {"id":"63","sap_abbreviation":"KNKLI","description":"Kreditkonto"},
        {"id":"64","sap_abbreviation":"GRUPP","description":"KundenkreditGrp"},
        {"id":"65","sap_abbreviation":"SBGRP","description":"Bearbeitergruppe"},
        {"id":"66","sap_abbreviation":"CTLPC","description":"Risikoklasse"},
        {"id":"67","sap_abbreviation":"CMWAE","description":"Währung"},
        {"id":"68","sap_abbreviation":"CMFRE","description":"Freigabedatum"},
        {"id":"69","sap_abbreviation":"CMNUP","description":"Nächste Prüfung"},
        {"id":"70","sap_abbreviation":"CMNGV","description":"Nächstes Datum"},
        {"id":"71","sap_abbreviation":"AMTBL","description":"Freigegeb Kreditwert"},
        {"id":"72","sap_abbreviation":"HITYP_PR","description":"HierTypPreisfindung"},
        {"id":"73","sap_abbreviation":"ABRVW","description":"Verwendung"},
        {"id":"74","sap_abbreviation":"ABDIS","description":"Dispobeh.Abrufarten"},
        {"id":"75","sap_abbreviation":"VGBEL","description":"Vorlagebeleg"},
        {"id":"76","sap_abbreviation":"OBJNR","description":"Objektnummer Kopf"},
        {"id":"77","sap_abbreviation":"BUKRS_VF","description":"FaktBuchungskreis"},
        {"id":"78","sap_abbreviation":"TAXK1","description":"Abweich.Steuerklasse"},
        {"id":"79","sap_abbreviation":"TAXK2","description":"Steuerklassifi.2-Kd"},
        {"id":"80","sap_abbreviation":"TAXK3","description":"Steuerklassifi.3-Kd"},
        {"id":"81","sap_abbreviation":"TAXK4","description":"Steuerklassifi.4-Kd"},
        {"id":"82","sap_abbreviation":"TAXK5","description":"Steuerklassifi.5-Kd"},
        {"id":"83","sap_abbreviation":"TAXK6","description":"Steuerklassifi.6-Kd"},
        {"id":"84","sap_abbreviation":"TAXK7","description":"Steuerklassifi.7-Kd"},
        {"id":"85","sap_abbreviation":"TAXK8","description":"Steuerklassifi.8-Kd"},
        {"id":"86","sap_abbreviation":"TAXK9","description":"Steuerklassifi.9-Kd"},
        {"id":"87","sap_abbreviation":"XBLNR","description":"Referenz"},
        {"id":"88","sap_abbreviation":"ZUONR","description":"Zuordnung"},
        {"id":"89","sap_abbreviation":"VGTYP","description":"Vorgängerbelegtyp"},
        {"id":"90","sap_abbreviation":"KALSM_CH","description":"Suchschema"},
        {"id":"91","sap_abbreviation":"AGRZR","description":"Abgrenzungszeitraum"},
        {"id":"92","sap_abbreviation":"AUFNR","description":"Auftrag"},
        {"id":"93","sap_abbreviation":"QMNUM","description":"Meldung"},
        {"id":"94","sap_abbreviation":"VBELN_GRP","description":"Gruppenkontrakt"},
        {"id":"95","sap_abbreviation":"SCHEME_GRP","description":"GrpReferenzschema"},
        {"id":"96","sap_abbreviation":"ABRUF_PART","description":"Abrufprüfung Partner"},
        {"id":"97","sap_abbreviation":"ABHOD","description":"Abholdatum"},
        {"id":"98","sap_abbreviation":"ABHOV","description":"Abholzeit"},
        {"id":"99","sap_abbreviation":"ABHOB","description":"Abholzeit"},
        {"id":"100","sap_abbreviation":"RPLNR","description":"Ratenplannummer"},
        {"id":"101","sap_abbreviation":"VZEIT","description":"Wunschlieferuhrzeit"},
        {"id":"102","sap_abbreviation":"STCEG_L","description":"SteuerEmpfangsland"},
        {"id":"103","sap_abbreviation":"LANDTX","description":"SteuerAbgangsland"},
        {"id":"104","sap_abbreviation":"XEGDR","description":"EU-Dreiecksgeschäft"},
        {"id":"105","sap_abbreviation":"ENQUEUE_GRP","description":"Gruppenkontrakt sperren bis alle Unterkontrakte aktualisiert"},
        {"id":"106","sap_abbreviation":"DAT_FZAU","description":"Datum AuftragsFZ"},
        {"id":"107","sap_abbreviation":"FMBDAT","description":"Mat.Bereitst.Datum"},
        {"id":"108","sap_abbreviation":"VSNMR_V","description":"Version"},
        {"id":"109","sap_abbreviation":"HANDLE","description":"Handle"},
        {"id":"110","sap_abbreviation":"PROLI","description":"GgAbwicklungsprofil"},
        {"id":"111","sap_abbreviation":"CONT_DG","description":"Enthält Gefahrgüter"},
        {"id":"112","sap_abbreviation":"CRM_GUID","description":"char70"},
        {"id":"113","sap_abbreviation":"UPD_TMSTMP","description":"Zeitstempel"},
        {"id":"114","sap_abbreviation":"MSR_ID","description":"Prozess-ID-Nummer"},
        {"id":"115","sap_abbreviation":"TM_CTRL_KEY","description":"Steuerschlüssel"},
        {"id":"116","sap_abbreviation":"HANDOVERLOC","description":"Übergabeort"},
        {"id":"117","sap_abbreviation":"PSM_BUDAT","description":"Buchungsdatum"},
        {"id":"118","sap_abbreviation":"SWENR","description":"Wirtschaftseinheit"},
        {"id":"119","sap_abbreviation":"SMENR","description":"Einheitennummer"},
        {"id":"120","sap_abbreviation":"PHASE","description":"Verkaufsphase"},
        {"id":"121","sap_abbreviation":"MTLAUR","description":"Zieleinkommen"},
        {"id":"122","sap_abbreviation":"STAGE","description":"Bauabschnitt"},
        {"id":"123","sap_abbreviation":"HB_CONT_REASON","description":"Vorbehaltsgrund"},
        {"id":"124","sap_abbreviation":"HB_EXPDATE","description":"Ablaufdatum"},
        {"id":"125","sap_abbreviation":"HB_RESDATE","description":"Aufhebungsdatum"},
        {"id":"126","sap_abbreviation":"MILL_APPL_ID","description":"Applikations-ID"},
        {"id":"127","sap_abbreviation":"LOGSYSB","description":"Log. System Beleg"},
        {"id":"128","sap_abbreviation":"KALCD","description":"Schema Kampagnenf."},
        {"id":"129","sap_abbreviation":"MULTI","description":"Mehrere Promotions"},
        {"id":"130","sap_abbreviation":"SPPAYM","description":"Zahlweg"},
        {"id":"131","sap_abbreviation":"WTYSC_CLM_HDR","description":"Antragskopf"},
        {"id":"132","sap_abbreviation":"ZZFFPNR","description":"MetallabsicherungsNr"},
        {"id":"133","sap_abbreviation":"ZZZOLL","description":"Flag ohne Zoll"},
        {"id":"134","sap_abbreviation":"POSNR","description":"Position"},
        {"id":"135","sap_abbreviation":"MATNR","description":"Material"},
        {"id":"136","sap_abbreviation":"MATWA","description":"Eingeg. Material"},
        {"id":"137","sap_abbreviation":"PMATN","description":"Preismaterial"},
        {"id":"138","sap_abbreviation":"CHARG","description":"Charge"},
        {"id":"139","sap_abbreviation":"MATKL","description":"Warengruppe"},
        {"id":"140","sap_abbreviation":"ARKTX","description":"Bezeichnung"},
        {"id":"141","sap_abbreviation":"PSTYV","description":"Positionstyp"},
        {"id":"142","sap_abbreviation":"POSAR","description":"Positionsart"},
        {"id":"143","sap_abbreviation":"LFREL","description":"Pos lieferrelevant"},
        {"id":"144","sap_abbreviation":"FKREL","description":"Fakturarelevanz"},
        {"id":"145","sap_abbreviation":"UEPOS","description":"Übergeordn. Position"},
        {"id":"146","sap_abbreviation":"GRPOS","description":"Alternativ zu Pos."},
        {"id":"147","sap_abbreviation":"ABGRU","description":"Absagegrund"},
        {"id":"148","sap_abbreviation":"PRODH","description":"Produkthierarchie"},
        {"id":"149","sap_abbreviation":"ZWERT","description":"Zielwert Rahmenvertr"},
        {"id":"150","sap_abbreviation":"ZMENG","description":"Zielmenge"},
        {"id":"151","sap_abbreviation":"ZIEME","description":"Zielmengeneinheit"},
        {"id":"152","sap_abbreviation":"UMZIZ","description":"Zähler Ziel -> Lager"},
        {"id":"153","sap_abbreviation":"UMZIN","description":"Nenner Ziel -> Lager"},
        {"id":"154","sap_abbreviation":"MEINS","description":"Basismengeneinheit"},
        {"id":"155","sap_abbreviation":"SMENG","description":"Staffelmenge"},
        {"id":"156","sap_abbreviation":"ABLFZ","description":"Rundungsmenge Lief."},
        {"id":"157","sap_abbreviation":"ABDAT","description":"Abstimmdatum"},
        {"id":"158","sap_abbreviation":"ABSFZ","description":"Abweichung absolut"},
        {"id":"159","sap_abbreviation":"POSEX","description":"Bestellposition"},
        {"id":"160","sap_abbreviation":"KDMAT","description":"Kundenmaterial"},
        {"id":"161","sap_abbreviation":"KBVER","description":"Abweichung proz."},
        {"id":"162","sap_abbreviation":"KEVER","description":"Anz.Tage Abw."},
        {"id":"163","sap_abbreviation":"VKGRU","description":"Rep.: Klassifizierung von Positionen"},
        {"id":"164","sap_abbreviation":"VKAUS","description":"Verwendung"},
        {"id":"165","sap_abbreviation":"GRKOR","description":"Liefergruppe"},
        {"id":"166","sap_abbreviation":"FMENG","description":"Menge ist fix"},
        {"id":"167","sap_abbreviation":"UEBTK","description":"Tol. unbegrenzt"},
        {"id":"168","sap_abbreviation":"UEBTO","description":"Tol.Überlieferung"},
        {"id":"169","sap_abbreviation":"UNTTO","description":"Tol.Unterlieferung"},
        {"id":"170","sap_abbreviation":"FAKSP","description":"Fakturasperre"},
        {"id":"171","sap_abbreviation":"ATPKZ","description":"Austauschteil"},
        {"id":"172","sap_abbreviation":"RKFKF","description":"Fakturierform RK\/PPS"},
        {"id":"173","sap_abbreviation":"ANTLF","description":"Max.Teillieferungen"},
        {"id":"174","sap_abbreviation":"KZTLF","description":"Teillieferung\/Pos."},
        {"id":"175","sap_abbreviation":"CHSPL","description":"Chargensplit erlaubt"},
        {"id":"176","sap_abbreviation":"KWMENG","description":"Auftragsmenge"},
        {"id":"177","sap_abbreviation":"LSMENG","description":"Liefersollmenge"},
        {"id":"178","sap_abbreviation":"KBMENG","description":"Kum.bestätigte Menge"},
        {"id":"179","sap_abbreviation":"KLMENG","description":"Kum.bestätigte Menge"},
        {"id":"180","sap_abbreviation":"VRKME","description":"Verkaufsmengeneinh."},
        {"id":"181","sap_abbreviation":"UMVKZ","description":"Zaehler"},
        {"id":"182","sap_abbreviation":"UMVKN","description":"Nenner"},
        {"id":"183","sap_abbreviation":"BRGEW","description":"Bruttogewicht"},
        {"id":"184","sap_abbreviation":"NTGEW","description":"Nettogewicht"},
        {"id":"185","sap_abbreviation":"GEWEI","description":"Gewichtseinheit"},
        {"id":"186","sap_abbreviation":"VOLUM","description":"Volumen"},
        {"id":"187","sap_abbreviation":"VOLEH","description":"Volumeneinheit"},
        {"id":"188","sap_abbreviation":"VBELV","description":"Verursacher"},
        {"id":"189","sap_abbreviation":"POSNV","description":"Position"},
        {"id":"190","sap_abbreviation":"VGPOS","description":"Vorlage Gesch. Pos."},
        {"id":"191","sap_abbreviation":"VOREF","description":"Vollreferenz"},
        {"id":"192","sap_abbreviation":"UPFLU","description":"Update Belegfluß"},
        {"id":"193","sap_abbreviation":"ERLRE","description":"Erledigungsregel"},
        {"id":"194","sap_abbreviation":"LPRIO","description":"Lieferpriorität"},
        {"id":"195","sap_abbreviation":"WERKS","description":"Werk"},
        {"id":"196","sap_abbreviation":"LGORT","description":"Lagerort"},
        {"id":"197","sap_abbreviation":"VSTEL","description":"Versandstelle\/Annahmestelle"},
        {"id":"198","sap_abbreviation":"ROUTE","description":"Route"},
        {"id":"199","sap_abbreviation":"STKEY","description":"Herkunft Stückliste"},
        {"id":"200","sap_abbreviation":"STDAT","description":"StichdatumStückliste"},
        {"id":"201","sap_abbreviation":"STLNR","description":"Stückliste"},
        {"id":"202","sap_abbreviation":"STPOS","description":"Stücklistenpositionsnummer"},
        {"id":"203","sap_abbreviation":"AWAHR","description":"Auftr.Wahrscheinl"},
        {"id":"204","sap_abbreviation":"TAXM1","description":"Steuerklassifikation"},
        {"id":"205","sap_abbreviation":"TAXM2","description":"Steuerklassifikation"},
        {"id":"206","sap_abbreviation":"TAXM3","description":"Steuerklassifikation"},
        {"id":"207","sap_abbreviation":"TAXM4","description":"Steuerklassifikation"},
        {"id":"208","sap_abbreviation":"TAXM5","description":"Steuerklassifikation"},
        {"id":"209","sap_abbreviation":"TAXM6","description":"Steuerklassifikation"},
        {"id":"210","sap_abbreviation":"TAXM7","description":"Steuerklassifikation"},
        {"id":"211","sap_abbreviation":"TAXM8","description":"Steuerklassifikation"},
        {"id":"212","sap_abbreviation":"TAXM9","description":"Steuerklassifikation"},
        {"id":"213","sap_abbreviation":"VBEAF","description":"Bearbeitungszeit fix"},
        {"id":"214","sap_abbreviation":"VBEAV","description":"Bearbeitungszeit var"},
        {"id":"215","sap_abbreviation":"VGREF","description":"Vorgängerbeleg ist aus Referenz entst."},
        {"id":"216","sap_abbreviation":"NETPR","description":"Nettopreis"},
        {"id":"217","sap_abbreviation":"KPEIN","description":"Preiseinheit"},
        {"id":"218","sap_abbreviation":"KMEIN","description":"Mengeneinheit"},
        {"id":"219","sap_abbreviation":"SHKZG","description":"Retoure"},
        {"id":"220","sap_abbreviation":"SKTOF","description":"Skontofähig"},
        {"id":"221","sap_abbreviation":"MTVFP","description":"Verfügbarkeitsprüf."},
        {"id":"222","sap_abbreviation":"SUMBD","description":"Summierung Bedarf"},
        {"id":"223","sap_abbreviation":"KONDM","description":"Materialgruppe"},
        {"id":"224","sap_abbreviation":"KTGRM","description":"Kontierungsgr. Mat."},
        {"id":"225","sap_abbreviation":"BONUS","description":"Bonusgruppe"},
        {"id":"226","sap_abbreviation":"PROVG","description":"Provisionsgruppe"},
        {"id":"227","sap_abbreviation":"EANNR","description":"EAN-Nummer"},
        {"id":"228","sap_abbreviation":"PRSOK","description":"Preisfindung"},
        {"id":"229","sap_abbreviation":"BWTAR","description":"Bewertungsart"},
        {"id":"230","sap_abbreviation":"BWTEX","description":"getrennte Bewertung"},
        {"id":"231","sap_abbreviation":"XCHPF","description":"Chargenpflicht"},
        {"id":"232","sap_abbreviation":"XCHAR","description":"Chargenführung"},
        {"id":"233","sap_abbreviation":"LFMNG","description":"Mindestliefermenge"},
        {"id":"234","sap_abbreviation":"WAVWR","description":"Verrechnungswert"},
        {"id":"235","sap_abbreviation":"KZWI1","description":"Zwischensumme 1"},
        {"id":"236","sap_abbreviation":"KZWI2","description":"Zwischensumme 2"},
        {"id":"237","sap_abbreviation":"KZWI3","description":"Zwischensumme 3"},
        {"id":"238","sap_abbreviation":"KZWI4","description":"Zwischensumme 4"},
        {"id":"239","sap_abbreviation":"KZWI5","description":"Zwischensumme 5"},
        {"id":"240","sap_abbreviation":"KZWI6","description":"Zwischensumme 6"},
        {"id":"241","sap_abbreviation":"STCUR","description":"Kurs Statistken"},
        {"id":"242","sap_abbreviation":"EAN11","description":"EAN\/UPC-Code"},
        {"id":"243","sap_abbreviation":"FIXMG","description":"Termin u.Menge fix"},
        {"id":"244","sap_abbreviation":"PRCTR","description":"Profitcenter"},
        {"id":"245","sap_abbreviation":"MVGR1","description":"Materialgruppe 1"},
        {"id":"246","sap_abbreviation":"MVGR2","description":"Materialgruppe 2"},
        {"id":"247","sap_abbreviation":"MVGR3","description":"Materialgruppe 3"},
        {"id":"248","sap_abbreviation":"MVGR4","description":"Materialgruppe 4"},
        {"id":"249","sap_abbreviation":"MVGR5","description":"Materialgruppe 5"},
        {"id":"250","sap_abbreviation":"KMPMG","description":"Komponentenmenge"},
        {"id":"251","sap_abbreviation":"SUGRD","description":"Substitutionsgrund"},
        {"id":"252","sap_abbreviation":"SOBKZ","description":"Sonderbestand"},
        {"id":"253","sap_abbreviation":"VPZUO","description":"Zuordnungskennz"},
        {"id":"254","sap_abbreviation":"PAOBJNR","description":"Ergebnisobjektnummer"},
        {"id":"255","sap_abbreviation":"VPMAT","description":"Vorplanmaterial"},
        {"id":"256","sap_abbreviation":"VPWRK","description":"Vorplanungswerk"},
        {"id":"257","sap_abbreviation":"PRBME","description":"Produktgr.ME"},
        {"id":"258","sap_abbreviation":"UMREF","description":"Umrechnung"},
        {"id":"259","sap_abbreviation":"KNTTP","description":"Kontierungstyp"},
        {"id":"260","sap_abbreviation":"KZVBR","description":"Verbrauch"},
        {"id":"261","sap_abbreviation":"SERNR","description":"Seriennummer"},
        {"id":"262","sap_abbreviation":"OBJNR","description":"Objektnr. Position"},
        {"id":"263","sap_abbreviation":"ABGRS","description":"Abgrenzungsschlüssel"},
        {"id":"264","sap_abbreviation":"BEDAE","description":"Bedarfsart"},
        {"id":"265","sap_abbreviation":"CMPRE","description":"Kreditpreis"},
        {"id":"266","sap_abbreviation":"CMTFG","description":"Teilfreigabe"},
        {"id":"267","sap_abbreviation":"CMPNT","description":"aktive Forderung"},
        {"id":"268","sap_abbreviation":"CMKUA","description":"Kurs Kreditdaten"},
        {"id":"269","sap_abbreviation":"CUOBJ","description":"Konfiguration"},
        {"id":"270","sap_abbreviation":"CUOBJ_CH","description":"Interne Objektnummer"},
        {"id":"271","sap_abbreviation":"CEPOK","description":"ErwarteterPreis"},
        {"id":"272","sap_abbreviation":"KOUPD","description":"Konditionsupdate"},
        {"id":"273","sap_abbreviation":"SERAIL","description":"Serialnummernprofil"},
        {"id":"274","sap_abbreviation":"ANZSN","description":"Anzahl Serialnummern"},
        {"id":"275","sap_abbreviation":"NACHL","description":"kein WE beim Kunden"},
        {"id":"276","sap_abbreviation":"MAGRV","description":"Materialgruppe PM"},
        {"id":"277","sap_abbreviation":"MPROK","description":"ManuellerPreis"},
        {"id":"278","sap_abbreviation":"PROSA","description":"ArtikelSel. aktiv"},
        {"id":"279","sap_abbreviation":"UEPVW","description":"Verwendung UEPOS"},
        {"id":"280","sap_abbreviation":"KALNR","description":"Kalkulationsnummer"},
        {"id":"281","sap_abbreviation":"KLVAR","description":"Kalkulationsvariante"},
        {"id":"282","sap_abbreviation":"SPOSN","description":"Positionsnr"},
        {"id":"283","sap_abbreviation":"KOWRR","description":"Wert statistisch"},
        {"id":"284","sap_abbreviation":"STADAT","description":"Statistikdatum"},
        {"id":"285","sap_abbreviation":"EXART","description":"Geschäftsart"},
        {"id":"286","sap_abbreviation":"PREFE","description":"Berecht.f.Zollverg."},
        {"id":"287","sap_abbreviation":"KNUMH","description":"Nr. Kond.Satz Charge"},
        {"id":"288","sap_abbreviation":"CLINT","description":"Int.Klasnr"},
        {"id":"289","sap_abbreviation":"CHMVS","description":"Mengenvorschlag"},
        {"id":"290","sap_abbreviation":"STLTY","description":"Stücklistentyp"},
        {"id":"291","sap_abbreviation":"STLKN","description":"Knoten Position"},
        {"id":"292","sap_abbreviation":"STPOZ","description":"Zähler"},
        {"id":"293","sap_abbreviation":"STMAN","description":"Konfig. inkonsistent"},
        {"id":"294","sap_abbreviation":"ZSCHL_K","description":"Zuschlagsschlüssel"},
        {"id":"295","sap_abbreviation":"KALSM_K","description":"Kalkulationsschema"},
        {"id":"296","sap_abbreviation":"KALVAR","description":"Kalkulationsvariante"},
        {"id":"297","sap_abbreviation":"KOSCH","description":"KontingentSchema"},
        {"id":"298","sap_abbreviation":"UPMAT","description":"PreisMat HauptPositn"},
        {"id":"299","sap_abbreviation":"UKONM","description":"MaterialGr HauptPos"},
        {"id":"300","sap_abbreviation":"MFRGR","description":"MatFraGruppe"},
        {"id":"301","sap_abbreviation":"PLAVO","description":"Planabrufvorschrift"},
        {"id":"302","sap_abbreviation":"KANNR","description":"Sequenz-Nummer"},
        {"id":"303","sap_abbreviation":"CMPRE_FLT","description":"Kreditpreis"},
        {"id":"304","sap_abbreviation":"ABFOR","description":"Absicherungsform"},
        {"id":"305","sap_abbreviation":"ABGES","description":"abgesichert"},
        {"id":"306","sap_abbreviation":"J_1BCFOP","description":"CFOP"},
        {"id":"307","sap_abbreviation":"J_1BTAXLW1","description":"Gesetz ICMS"},
        {"id":"308","sap_abbreviation":"J_1BTAXLW2","description":"Gesetz IPI"},
        {"id":"309","sap_abbreviation":"J_1BTXSDC","description":"Steuerkennzeichen"},
        {"id":"310","sap_abbreviation":"WKTNR","description":"Wertkontraktnummer"},
        {"id":"311","sap_abbreviation":"WKTPS","description":"Wertkontraktposition"},
        {"id":"312","sap_abbreviation":"SKOPF","description":"Baustein"},
        {"id":"313","sap_abbreviation":"KZBWS","description":"Bewertung SondBest"},
        {"id":"314","sap_abbreviation":"WGRU1","description":"Warengruppe 1"},
        {"id":"315","sap_abbreviation":"WGRU2","description":"Warengruppe 2"},
        {"id":"316","sap_abbreviation":"KNUMA_PI","description":"Promotion"},
        {"id":"317","sap_abbreviation":"KNUMA_AG","description":"Verkaufsaktion"},
        {"id":"318","sap_abbreviation":"KZFME","description":"Führende Mengeneinh."},
        {"id":"319","sap_abbreviation":"LSTANR","description":"Liefersteuerung Naturalrabatt"},
        {"id":"320","sap_abbreviation":"TECHS","description":"Standardbewertung"},
        {"id":"321","sap_abbreviation":"MWSBP","description":"Steuerbetrag"},
        {"id":"322","sap_abbreviation":"BERID","description":"Dispobereich"},
        {"id":"323","sap_abbreviation":"PCTRF","description":"Profit Center Faktur"},
        {"id":"324","sap_abbreviation":"LOGSYS_EXT","description":"Logisches System"},
        {"id":"325","sap_abbreviation":"J_1BTAXLW3","description":"ISS-Gesetz"},
        {"id":"326","sap_abbreviation":"J_1BTAXLW4","description":"COFINS Gesetz"},
        {"id":"327","sap_abbreviation":"J_1BTAXLW5","description":"PIS-Gesetz"},
        {"id":"328","sap_abbreviation":"STOCKLOC","description":"Lokation"},
        {"id":"329","sap_abbreviation":"SLOCTYPE","description":"Lokationstyp"},
        {"id":"330","sap_abbreviation":"MSR_RET_REASON","description":"Retourengrund"},
        {"id":"331","sap_abbreviation":"MSR_REFUND_CODE","description":"RückerstattSchlü."},
        {"id":"332","sap_abbreviation":"MSR_APPROV_BLOCK","description":"Genehmigung"},
        {"id":"333","sap_abbreviation":"NRAB_KNUMH","description":"Nr. Konditionssatz"},
        {"id":"334","sap_abbreviation":"TRMRISK_RELEVANT","description":"Risikorelevanz"},
        {"id":"335","sap_abbreviation":"SGT_RCAT","description":"Bedarfssegment"},
        {"id":"336","sap_abbreviation":"HANDOVERDATE","description":"Übergabedatum"},
        {"id":"337","sap_abbreviation":"HANDOVERTIME","description":"Übergabezeit"},
        {"id":"338","sap_abbreviation":"TC_AUT_DET","description":"Steuerkennzeichen automatisch ermittelt"},
        {"id":"339","sap_abbreviation":"MANUAL_TC_REASON","description":"Grund für manuelles Steuerkennzeichen"},
        {"id":"340","sap_abbreviation":"FISCAL_INCENTIVE","description":"Art des steuerlichen Anreizes"},
        {"id":"341","sap_abbreviation":"TAX_SUBJECT_ST","description":"Steuerpflicht (Substituicao Tributaria)"},
        {"id":"342","sap_abbreviation":"FISCAL_INCENTIVE_ID","description":"Anreiz-ID"},
        {"id":"343","sap_abbreviation":"SPCSTO","description":"NF CFOP Sonderfall"},
        {"id":"344","sap_abbreviation":"REVACC_REFID","description":"Erlösbuchhaltung: Ref.-ID"},
        {"id":"345","sap_abbreviation":"REVACC_REFTYPE","description":"ErlösbuchhaltReferenztyp"},
        {"id":"346","sap_abbreviation":"SESSION_CREATION_DATE","description":"Session angelegt am"},
        {"id":"347","sap_abbreviation":"SESSION_CREATION_TIME","description":"Session angelegt um"},
        {"id":"348","sap_abbreviation":"\/BEV1\/SRFUND","description":"Analyse\/Absagegrund"},
        {"id":"349","sap_abbreviation":"AUFPL_OLC","description":"Plannummer Vorgänge"},
        {"id":"350","sap_abbreviation":"APLZL_OLC","description":"Zähler"},
        {"id":"351","sap_abbreviation":"FERC_IND","description":"Kz. Meldewesen"},
        {"id":"352","sap_abbreviation":"FONDS","description":"Fonds"},
        {"id":"353","sap_abbreviation":"FISTL","description":"Finanzstelle"},
        {"id":"354","sap_abbreviation":"FKBER","description":"Funktionsbereich"},
        {"id":"355","sap_abbreviation":"GRANT_NBR","description":"Förderung"},
        {"id":"356","sap_abbreviation":"IUID_RELEVANT","description":"IUID-relevant für Kunde"},
        {"id":"357","sap_abbreviation":"MILL_SE_GPOSN","description":"globale Position"},
        {"id":"358","sap_abbreviation":"PRS_OBJNR","description":"Auftragsabwicklung: Objektnummer"},
        {"id":"359","sap_abbreviation":"PRS_SD_SPSNR","description":"Standard-PSP-Element"},
        {"id":"360","sap_abbreviation":"PRS_WORK_PERIOD","description":"Leistungsperiode"},
        {"id":"361","sap_abbreviation":"PARGB","description":"PartnerGsber"},
        {"id":"362","sap_abbreviation":"AUFPL_OAA","description":"Plannummer Vorgänge"},
        {"id":"363","sap_abbreviation":"APLZL_OAA","description":"Zähler"},
        {"id":"364","sap_abbreviation":"ARSNUM","description":"Reservierung"},
        {"id":"365","sap_abbreviation":"ARSPOS","description":"Pos.-Nr. der Reservierung"},
        {"id":"366","sap_abbreviation":"WTYSC_CLMITEM","description":"Antragspositionsnummer"},
        {"id":"367","sap_abbreviation":"ZZQMNUM","description":"Meldung"},
        {"id":"368","sap_abbreviation":"ZZPRGBZ","description":"Lieferdatum"},
        {"id":"369","sap_abbreviation":"ZZETDAT","description":"Lieferdatum"},
        {"id":"370","sap_abbreviation":"\/WSW\/SPEEDI_F1","description":"Datum"},
        {"id":"371","sap_abbreviation":"\/WSW\/SPEEDI_F2","description":"Character Länge 1"},
        {"id":"372","sap_abbreviation":"\/WSW\/SPEEDI_F3","description":"Character Länge 1"},
        {"id":"373","sap_abbreviation":"\/WSW\/SPEEDI_F4","description":"Character Länge 1"},
        {"id":"374","sap_abbreviation":"\/WSW\/SPEEDI_F5","description":"Character Länge 1"},
        {"id":"375","sap_abbreviation":"ZZCM2PST","description":"m2 pro Stück"},
        {"id":"376","sap_abbreviation":"ZZCALU_F","description":"Alufaktor"},
        {"id":"377","sap_abbreviation":"ZZCM2GES","description":"m² pro Pos"},
        {"id":"378","sap_abbreviation":"VBELN","description":"Vertriebsbeleg"},
        {"id":"379","sap_abbreviation":"POSNR","description":"Position (SD)"},
        {"id":"380","sap_abbreviation":"KONDA","description":"Preisgruppe"},
        {"id":"381","sap_abbreviation":"KDGRP","description":"Kundengruppe"},
        {"id":"382","sap_abbreviation":"BZIRK","description":"Kundenbezirk"},
        {"id":"383","sap_abbreviation":"PLTYP","description":"Preisliste"},
        {"id":"384","sap_abbreviation":"INCO1","description":"Incoterms"},
        {"id":"385","sap_abbreviation":"INCO2","description":"Incoterms Teil 2"},
        {"id":"386","sap_abbreviation":"KZAZU","description":"AuftrZusammenführung"},
        {"id":"387","sap_abbreviation":"PERFK","description":"Rechnungstermine"},
        {"id":"388","sap_abbreviation":"PERRL","description":"RechListenTermine"},
        {"id":"389","sap_abbreviation":"MRNKZ","description":"Rechnungsnachbearb."},
        {"id":"390","sap_abbreviation":"KURRF","description":"Kurs f.Buchhaltung"},
        {"id":"391","sap_abbreviation":"VALTG","description":"Zusätzl. Valutatage"},
        {"id":"392","sap_abbreviation":"VALDT","description":"Valuta-Fixdatum"},
        {"id":"393","sap_abbreviation":"ZTERM","description":"Zahlungsbedingung"},
        {"id":"394","sap_abbreviation":"ZLSCH","description":"Zahlweg"},
        {"id":"395","sap_abbreviation":"KTGRD","description":"Kontierungsgr. Deb."},
        {"id":"396","sap_abbreviation":"KURSK","description":"Kurs"},
        {"id":"397","sap_abbreviation":"PRSDT","description":"Preisdatum"},
        {"id":"398","sap_abbreviation":"FKDAT","description":"Fakturadatum"},
        {"id":"399","sap_abbreviation":"FBUDA","description":"Leistungserst.Dat"},
        {"id":"400","sap_abbreviation":"GJAHR","description":"Geschäftsjahr"},
        {"id":"401","sap_abbreviation":"POPER","description":"Buchungsperiode"},
        {"id":"402","sap_abbreviation":"STCUR","description":"Kurs Statistiken"},
        {"id":"403","sap_abbreviation":"MSCHL","description":"Mahnschlüssel"},
        {"id":"404","sap_abbreviation":"MANSP","description":"Mahnsperre"},
        {"id":"405","sap_abbreviation":"FPLNR","description":"Fakturierungsplannummer"},
        {"id":"406","sap_abbreviation":"WAKTION","description":"Aktion"},
        {"id":"407","sap_abbreviation":"ABSSC","description":"Absicherungsschema"},
        {"id":"408","sap_abbreviation":"LCNUM","description":"Finanzdokumentnummer"},
        {"id":"409","sap_abbreviation":"J_1AFITP","description":"Steuerart"},
        {"id":"410","sap_abbreviation":"J_1ARFZ","description":"Grund 0 MwSt."},
        {"id":"411","sap_abbreviation":"J_1AREGIO","description":"Region"},
        {"id":"412","sap_abbreviation":"J_1AGICD","description":"Tätigkeit BE-Steuer"},
        {"id":"413","sap_abbreviation":"J_1ADTYP","description":"Verteilungsart"},
        {"id":"414","sap_abbreviation":"J_1ATXREL","description":"Steuerrel.Klass"},
        {"id":"415","sap_abbreviation":"ABTNR","description":"Abteilung"},
        {"id":"416","sap_abbreviation":"EMPST","description":"Empfangsstelle"},
        {"id":"417","sap_abbreviation":"BSTKD","description":"Bestellnummer"},
        {"id":"418","sap_abbreviation":"BSTKD_E","description":"Bestellnummer"},
        {"id":"419","sap_abbreviation":"BSTDK_E","description":"Bestelldatum"},
        {"id":"420","sap_abbreviation":"BSARK_E","description":"Bestellart"},
        {"id":"421","sap_abbreviation":"IHREZ_E","description":"Ihr Zeichen"},
        {"id":"422","sap_abbreviation":"POSEX_E","description":"Bestellpositionsnr."},
        {"id":"423","sap_abbreviation":"KURSK_DAT","description":"Umrechnungsdatum"},
        {"id":"424","sap_abbreviation":"KURRF_DAT","description":"Umrechnungsdatum"},
        {"id":"425","sap_abbreviation":"KDKG1","description":"Konditionsgruppe 1"},
        {"id":"426","sap_abbreviation":"KDKG2","description":"Konditionsgruppe 2"},
        {"id":"427","sap_abbreviation":"KDKG3","description":"Konditionsgruppe 3"},
        {"id":"428","sap_abbreviation":"KDKG4","description":"Konditionsgruppe 4"},
        {"id":"429","sap_abbreviation":"KDKG5","description":"Konditionsgruppe 5"},
        {"id":"430","sap_abbreviation":"WKWAE","description":"Währung des zugeordneten Wertkontraktes"},
        {"id":"431","sap_abbreviation":"WKKUR","description":"Kurs"},
        {"id":"432","sap_abbreviation":"AKWAE","description":"Akkreditivwährung"},
        {"id":"433","sap_abbreviation":"AKKUR","description":"Umr.kurs Akkreditiv"},
        {"id":"434","sap_abbreviation":"AKPRZ","description":"Abschreibungsgrad"},
        {"id":"435","sap_abbreviation":"J_1AINDXP","description":"Inflationsindex"},
        {"id":"436","sap_abbreviation":"J_1AIDATEP","description":"Basisdat.Indizier."},
        {"id":"437","sap_abbreviation":"BSTKD_M","description":"Bestellnummer"},
        {"id":"438","sap_abbreviation":"DELCO","description":"Lieferzeit"},
        {"id":"439","sap_abbreviation":"FFPRF","description":"DPP-Profil"},
        {"id":"440","sap_abbreviation":"BEMOT","description":"Berechnungsmotiv"},
        {"id":"441","sap_abbreviation":"FAKTF","description":"Fakturierform"},
        {"id":"442","sap_abbreviation":"RRREL","description":"Erlösrealisierungstyp"},
        {"id":"443","sap_abbreviation":"ACDATV","description":"Regel f. AbgrenzBeginndatum"},
        {"id":"444","sap_abbreviation":"VSART","description":"Versandart"},
        {"id":"445","sap_abbreviation":"TRATY","description":"Transportmittelart"},
        {"id":"446","sap_abbreviation":"TRMTYP","description":"Transportmittel"},
        {"id":"447","sap_abbreviation":"SDABW","description":"Sonderabwicklungskennz."},
        {"id":"448","sap_abbreviation":"WMINR","description":"Katalog"},
        {"id":"449","sap_abbreviation":"PODKZ","description":"LEB relevant"},
        {"id":"450","sap_abbreviation":"CAMPAIGN","description":"CGPL_GUID"},
        {"id":"451","sap_abbreviation":"VKONT","description":"Vertragskonto"},
        {"id":"452","sap_abbreviation":"DPBP_REF_FPLNR","description":"Fakturierungsplannummer"},
        {"id":"453","sap_abbreviation":"DPBP_REF_FPLTR","description":"Position"},
        {"id":"454","sap_abbreviation":"REVSP","description":"Erlösverteilungstyp"},
        {"id":"455","sap_abbreviation":"REVEVTYP","description":"Erlösereignistyp"},
        {"id":"456","sap_abbreviation":"FARR_RELTYPE","description":"Erlösbuchhaltungsart"},
        {"id":"457","sap_abbreviation":"VTREF","description":"Vertrag"},
        {"id":"458","sap_abbreviation":"_DATAAGING","description":"Datenfilterwert für Data Aging"},
        {"id":"459","sap_abbreviation":"J_1TPBUPL","description":""},
        {"id":"460","sap_abbreviation":"INCOV","description":"Incoterm-Version"},
        {"id":"461","sap_abbreviation":"INCO2_L","description":"Incoterms Standort 1"},
        {"id":"462","sap_abbreviation":"INCO3_L","description":"Incoterms Standort 2"},
        {"id":"463","sap_abbreviation":"PEROP_BEG","description":""},
        {"id":"464","sap_abbreviation":"PEROP_END","description":""},
        {"id":"465","sap_abbreviation":"STCODE","description":""},
        {"id":"466","sap_abbreviation":"FORMC1","description":""},
        {"id":"467","sap_abbreviation":"FORMC2","description":""},
        {"id":"468","sap_abbreviation":"STEUC","description":"Steuerungscode"},
        {"id":"469","sap_abbreviation":"COMPREAS","description":"Abkürzung Reklamationsgrund"},
        {"id":"470","sap_abbreviation":"MNDID","description":"Mandatsreferenz"},
        {"id":"471","sap_abbreviation":"PAY_TYPE","description":"Zahlungsart"},
        {"id":"472","sap_abbreviation":"SEPON","description":"SEPA-relevant"},
        {"id":"473","sap_abbreviation":"MNDVG","description":"SEPA-relevant"},
        {"id":"474","sap_abbreviation":"ABRLI","description":"Interner Lieferabruf"},
        {"id":"475","sap_abbreviation":"ABART","description":"Abrufart"},
        {"id":"476","sap_abbreviation":"DOCNUM","description":"IDoc-Nummer"},
        {"id":"477","sap_abbreviation":"ABEFZ","description":"Eingangs-FZ"},
        {"id":"478","sap_abbreviation":"ABRAB","description":"Abruf gültig ab"},
        {"id":"479","sap_abbreviation":"ABRBI","description":"Abruf gültig bis"},
        {"id":"480","sap_abbreviation":"LABNK","description":"Abruf"},
        {"id":"481","sap_abbreviation":"ABRDT","description":"Abrufdatum"},
        {"id":"482","sap_abbreviation":"TERSL","description":"Terminschlüssel"},
        {"id":"483","sap_abbreviation":"LFDKD","description":"Datum letzte Lief."},
        {"id":"484","sap_abbreviation":"LFNKD","description":"Letzte Lieferung"},
        {"id":"485","sap_abbreviation":"ABFDA","description":"Fert.freig.Anfang"},
        {"id":"486","sap_abbreviation":"ABFDE","description":"Fertigungsfr. Ende"},
        {"id":"487","sap_abbreviation":"ABMDA","description":"Materialfr. Anfang"},
        {"id":"488","sap_abbreviation":"ABMDE","description":"Materialfr. Ende"},
        {"id":"489","sap_abbreviation":"ABLLI","description":"Letzter Abruf"},
        {"id":"490","sap_abbreviation":"HIFFZ","description":"Höchste FFZ"},
        {"id":"491","sap_abbreviation":"HIFFZLI","description":"Abruf höchste FFZ"},
        {"id":"492","sap_abbreviation":"HIMFZ","description":"Höchste MFZ"},
        {"id":"493","sap_abbreviation":"HIMFZLI","description":"Abruf höchste MFZ"},
        {"id":"494","sap_abbreviation":"ERZEI","description":"Uhrzeit"},
        {"id":"495","sap_abbreviation":"HILFZ","description":"Höchste LFFZ"},
        {"id":"496","sap_abbreviation":"HILFZLI","description":"Abruf höchste LFFZ"},
        {"id":"497","sap_abbreviation":"ABHOR","description":"Feinabrufhorizont"},
        {"id":"498","sap_abbreviation":"GJKUN","description":"Gs.jahr des Kunden"},
        {"id":"499","sap_abbreviation":"VJKUN","description":"Vorjahr des Kunden"},
        {"id":"500","sap_abbreviation":"AKMFZ","description":"Aktuelle MFZ"},
        {"id":"501","sap_abbreviation":"AKFFZ","description":"Aktuelle FFZ"},
        {"id":"502","sap_abbreviation":"AKLFZ","description":"Akt.Lief.Freig.FZ"},
        {"id":"503","sap_abbreviation":"KRITB","description":"Kritischer Bestand"},
        {"id":"504","sap_abbreviation":"LABKY","description":"Bed.Status Schlüssel"},
        {"id":"505","sap_abbreviation":"VBRST","description":"Verbrauchsstelle"},
        {"id":"506","sap_abbreviation":"EDLLS","description":"EDL-Entnahme"},
        {"id":"507","sap_abbreviation":"EDLDT","description":"EDL-Datum"},
        {"id":"508","sap_abbreviation":"LFMKD","description":"Letzte_Lief.Menge"},
        {"id":"509","sap_abbreviation":"USR01","description":"Daten 1"},
        {"id":"510","sap_abbreviation":"USR02","description":"Daten 2"},
        {"id":"511","sap_abbreviation":"USR03","description":"Daten 3"},
        {"id":"512","sap_abbreviation":"USR04","description":"Daten 4"},
        {"id":"513","sap_abbreviation":"USR05","description":"Daten 5"},
        {"id":"514","sap_abbreviation":"CYEFZ","description":"FZ bei Nullstellung"},
        {"id":"515","sap_abbreviation":"CYDAT","description":"Datum Nullst. EFZ"},
        {"id":"516","sap_abbreviation":"MFLAUF","description":"Mat.frg.Laufzeit"},
        {"id":"517","sap_abbreviation":"MFEIN","description":"Materialfrg.Einheit"},
        {"id":"518","sap_abbreviation":"FFLAUF","description":"Fert.frg.Laufzeit"},
        {"id":"519","sap_abbreviation":"FFEIN","description":"Fert.frg.Einheit"},
        {"id":"520","sap_abbreviation":"ABRDT_ORG","description":"Abrufdatum"},
        {"id":"521","sap_abbreviation":"LFMAIS","description":"Pick-Up-Sheet"},
        {"id":"522","sap_abbreviation":"MAIDT","description":"PUS-Datum"},
        {"id":"523","sap_abbreviation":"\/WSW\/SPEEDI_F1","description":"Charakterfeld Länge 50"},
        {"id":"524","sap_abbreviation":"RFSTK","description":"Referenzstatus"},
        {"id":"525","sap_abbreviation":"RFGSK","description":"Gesamtreferenzstatus"},
        {"id":"526","sap_abbreviation":"BESTK","description":"bestätigt"},
        {"id":"527","sap_abbreviation":"LFSTK","description":"Lieferstatus"},
        {"id":"528","sap_abbreviation":"LFGSK","description":"Gesamtlieferstatus"},
        {"id":"529","sap_abbreviation":"WBSTK","description":"GesWarenbewegungStat"},
        {"id":"530","sap_abbreviation":"FKSTK","description":"Fakturastatus"},
        {"id":"531","sap_abbreviation":"FKSAK","description":"Fakt.Stat.auftragsb."},
        {"id":"532","sap_abbreviation":"BUCHK","description":"Buchungsstatus"},
        {"id":"533","sap_abbreviation":"ABSTK","description":"Absagestatus"},
        {"id":"534","sap_abbreviation":"GBSTK","description":"Gesamtstatus"},
        {"id":"535","sap_abbreviation":"KOSTK","description":"Gesamtstat. Kommiss."},
        {"id":"536","sap_abbreviation":"LVSTK","description":"Gesamtstatus WM-Akt."},
        {"id":"537","sap_abbreviation":"UVALS","description":"Positionsdaten"},
        {"id":"538","sap_abbreviation":"UVVLS","description":"Pos.daten Lieferung"},
        {"id":"539","sap_abbreviation":"UVFAS","description":"Pos.Dat.Faktura"},
        {"id":"540","sap_abbreviation":"UVALL","description":"Kopfdaten"},
        {"id":"541","sap_abbreviation":"UVVLK","description":"Kopfdaten Lieferung"},
        {"id":"542","sap_abbreviation":"UVFAK","description":"Kopfdaten Faktura"},
        {"id":"543","sap_abbreviation":"UVPRS","description":"Preisfindung"},
        {"id":"544","sap_abbreviation":"VBOBJ","description":"Vertriebsbelegobjekt"},
        {"id":"545","sap_abbreviation":"FKIVK","description":"SummenstatusIV"},
        {"id":"546","sap_abbreviation":"RELIK","description":"RechListStatus"},
        {"id":"547","sap_abbreviation":"UVK01","description":"Kopfreserve1"},
        {"id":"548","sap_abbreviation":"UVK02","description":"Kopfreserve2"},
        {"id":"549","sap_abbreviation":"UVK03","description":"Kopfreserve3"},
        {"id":"550","sap_abbreviation":"UVK04","description":"Kopfreserve4"},
        {"id":"551","sap_abbreviation":"UVK05","description":"Kopfreserve5"},
        {"id":"552","sap_abbreviation":"UVS01","description":"GesamtReserve1"},
        {"id":"553","sap_abbreviation":"UVS02","description":"GesamtReserve2"},
        {"id":"554","sap_abbreviation":"UVS03","description":"GesamtReserve3"},
        {"id":"555","sap_abbreviation":"UVS04","description":"GesamtReserve4"},
        {"id":"556","sap_abbreviation":"UVS05","description":"GesamtReserve5"},
        {"id":"557","sap_abbreviation":"PKSTK","description":"Packstatus"},
        {"id":"558","sap_abbreviation":"CMPSA","description":"Statische Prüfung"},
        {"id":"559","sap_abbreviation":"CMPSB","description":"Dynamische Prüfung"},
        {"id":"560","sap_abbreviation":"CMPSC","description":"Maximaler Wert"},
        {"id":"561","sap_abbreviation":"CMPSD","description":"Zahlungsbedingung"},
        {"id":"562","sap_abbreviation":"CMPSE","description":"Reviewdatum Kunde"},
        {"id":"563","sap_abbreviation":"CMPSF","description":"Überf. offene Posten"},
        {"id":"564","sap_abbreviation":"CMPSG","description":"Ältes. offene Posten"},
        {"id":"565","sap_abbreviation":"CMPSH","description":"Maximale Mahnstufe"},
        {"id":"566","sap_abbreviation":"CMPSI","description":"Finanzdokument"},
        {"id":"567","sap_abbreviation":"CMPSJ","description":"Warenkreditversichng"},
        {"id":"568","sap_abbreviation":"CMPSK","description":"Zahlungskarte"},
        {"id":"569","sap_abbreviation":"CMPSL","description":"Reserve"},
        {"id":"570","sap_abbreviation":"CMPS0","description":"Reserve"},
        {"id":"571","sap_abbreviation":"CMPS1","description":"Reserve"},
        {"id":"572","sap_abbreviation":"CMPS2","description":"Reserve"},
        {"id":"573","sap_abbreviation":"CMGST","description":"Gesamtstatus Kredit"},
        {"id":"574","sap_abbreviation":"TRSTA","description":"TransportDispoStat"},
        {"id":"575","sap_abbreviation":"KOQUK","description":"Quittierung Kommiss."},
        {"id":"576","sap_abbreviation":"COSTA","description":"Bestellbestätigung"},
        {"id":"577","sap_abbreviation":"SAPRL","description":"SAP-Release"},
        {"id":"578","sap_abbreviation":"UVPAS","description":"Pos.daten Verpacken"},
        {"id":"579","sap_abbreviation":"UVPIS","description":"Pos.daten Kommiss.\/Einl."},
        {"id":"580","sap_abbreviation":"UVWAS","description":"Pos.daten Warenbeweg."},
        {"id":"581","sap_abbreviation":"UVPAK","description":"Kopfdaten Verpacken"},
        {"id":"582","sap_abbreviation":"UVPIK","description":"Kopfdaten Kommiss.\/Einlagern"},
        {"id":"583","sap_abbreviation":"UVWAK","description":"Kopfdaten Warenbewegung"},
        {"id":"584","sap_abbreviation":"UVGEK","description":"Kopfdaten Gefahrgut"},
        {"id":"585","sap_abbreviation":"CMPSM","description":"Alter Kreditvektor"},
        {"id":"586","sap_abbreviation":"DCSTK","description":"Verzugstatus"},
        {"id":"587","sap_abbreviation":"VESTK","description":"HU eingelagert"},
        {"id":"588","sap_abbreviation":"VLSTK","description":"Status dez. Lager"},
        {"id":"589","sap_abbreviation":"RRSTA","description":"Erlösermittlg.status"},
        {"id":"590","sap_abbreviation":"BLOCK","description":"Kennzeichen: Beleg für Archivierung vorgemerkt"},
        {"id":"591","sap_abbreviation":"FSSTK","description":"G.Fakturasperrstatus"},
        {"id":"592","sap_abbreviation":"LSSTK","description":"G.Liefersperrestatus"},
        {"id":"593","sap_abbreviation":"SPSTG","description":"Gesamtsperrstatus"},
        {"id":"594","sap_abbreviation":"PDSTK","description":"Lieferempf.best. Status"},
        {"id":"595","sap_abbreviation":"FMSTK","description":"Status Funds Management"},
        {"id":"596","sap_abbreviation":"MANEK","description":"Manuelle Erledigung des Kontraktes"},
        {"id":"597","sap_abbreviation":"SPE_TMPID","description":"Temp. Anl."},
        {"id":"598","sap_abbreviation":"HDALL","description":"Gemerkt"},
        {"id":"599","sap_abbreviation":"HDALS","description":"Pos.zurück"},
        {"id":"600","sap_abbreviation":"CMPS_CM","description":"SAP Credit Management"},
        {"id":"601","sap_abbreviation":"CMPS_TE","description":"CM Status techn. Fehler"},
        {"id":"602","sap_abbreviation":"VBTYP_EXT","description":"Belegtyperweiterung"},
        {"id":"603","sap_abbreviation":"KPOSN","description":"Konditionspositionsnummer"},
        {"id":"604","sap_abbreviation":"STUNR","description":"Stufennummer"},
        {"id":"605","sap_abbreviation":"ZAEHK","description":"Zähler Konditionen"},
        {"id":"606","sap_abbreviation":"STUNR","description":"Stufennummer"},
        {"id":"607","sap_abbreviation":"KSCHL","description":"Konditionsart"},
        {"id":"608","sap_abbreviation":"KBETR","description":"Konditionsbetrag oder -prozentsatz"},
        {"id":"609","sap_abbreviation":"WAERS","description":"Währungsschlüssel"},
        {"id":"610","sap_abbreviation":"KPEIN","description":"Konditions-Preiseinheit"},
        {"id":"611","sap_abbreviation":"KMEIN","description":"Mengeneinheit Kondition im Beleg"}
]
    
    for sap_abbreviation_dictionary in sap_abbreviation_dictionary_list:
        sap_abbreviation_dictionary = SapAbbreviationDictionary(
            **sap_abbreviation_dictionary
        )
        sap_abbreviation_dictionary.save()

def createPatentTags():
    patent_tag_dict_list = [
        {'id': 1, 'name': 'crash can', 'alternative_name1': 'crash box', 'alternative_name2': 'absorber'},
        {'id': 2, 'name': 'cross member'},
        {'id': 3, 'name': 'adapter'},
        {'id': 4, 'name': 'crash management system', 'alternative_name1': 'cms'},
        {'id': 5, 'name': 'method'},
    ]

    for patent_tag_dict in patent_tag_dict_list:
        patent_tag = PatentTag(
            **patent_tag_dict
        )
        patent_tag.save()

def fillReferenceTables():
    createCurrencies()
    createNormTypes()
    createPartTypes()
    createPartPositions()
    createSemiFinishedProductTypes()
    createMaterialTypes()
    createPartSoldPriceComponentTypes()
    createPriceUploadSources()
    createSavingUnits()
    createPartSoldMaterialPriceTypes()
    createDerivativeTypes()
    createPredictionAccuracies()
    createProjectUserRoles()
    createProjectStaffCostTasks()
    createFakeRevisionsLmc(2022, 2023)
    createAutomatedExecutionInterval()
    createChangeRequestCostCategory()
    createChangeRequestRiskCategory()
    createChangeRequestRiskImpact()
    createChangeRequestRiskProbability()
    createFileExtensions()
    createFileTypes()
    createPartReleaseStatus()
    createProjectStatus()
    createProjectType()
    createTechnology()
    createSapAbbreviationDictionary()
    createPatentTags()