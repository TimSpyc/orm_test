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

    for file_type in file_type_list:
        file_type = FileType(
            name = file_type['name']
        )
        file_type.save()
        for file_extension in file_type['file_extension']:
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
        {"id":"1","sap_abbreviation":"MANDT","sap_full_text":"Mandant"},
        {"id":"2","sap_abbreviation":"VBELN","sap_full_text":"Verkaufsbeleg"},
        {"id":"3","sap_abbreviation":"ERDAT","sap_full_text":"Angelegt am"},
        {"id":"4","sap_abbreviation":"ERZET","sap_full_text":"Uhrzeit"},
        {"id":"5","sap_abbreviation":"ERNAM","sap_full_text":"Angelegt von"},
        {"id":"6","sap_abbreviation":"ANGDT","sap_full_text":"Angebot gültig von"},
        {"id":"7","sap_abbreviation":"BNDDT","sap_full_text":"Angebot gültig bis"},
        {"id":"8","sap_abbreviation":"AUDAT","sap_full_text":"Belegdatum"},
        {"id":"9","sap_abbreviation":"VBTYP","sap_full_text":"Vertriebsbelegtyp"},
        {"id":"10","sap_abbreviation":"TRVOG","sap_full_text":"Gr.Transakt.Vorgang"},
        {"id":"11","sap_abbreviation":"AUART","sap_full_text":"Verkaufsbelegart"},
        {"id":"12","sap_abbreviation":"AUGRU","sap_full_text":"Auftragsgrund"},
        {"id":"13","sap_abbreviation":"GWLDT","sap_full_text":"Gewährleistung"},
        {"id":"14","sap_abbreviation":"SUBMI","sap_full_text":"Submission"},
        {"id":"15","sap_abbreviation":"LIFSK","sap_full_text":"Liefersperre"},
        {"id":"16","sap_abbreviation":"FAKSK","sap_full_text":"Fakturasperre"},
        {"id":"17","sap_abbreviation":"NETWR","sap_full_text":"Nettowert"},
        {"id":"18","sap_abbreviation":"WAERK","sap_full_text":"Belegwährung"},
        {"id":"19","sap_abbreviation":"VKORG","sap_full_text":"Verkaufsorganisation"},
        {"id":"20","sap_abbreviation":"VTWEG","sap_full_text":"Vertriebsweg"},
        {"id":"21","sap_abbreviation":"SPART","sap_full_text":"Sparte"},
        {"id":"22","sap_abbreviation":"VKGRP","sap_full_text":"Verkäufergruppe"},
        {"id":"23","sap_abbreviation":"VKBUR","sap_full_text":"Verkaufsbüro"},
        {"id":"24","sap_abbreviation":"GSBER","sap_full_text":"Geschäftsbereich"},
        {"id":"25","sap_abbreviation":"GSKST","sap_full_text":"Geschäftsbereich"},
        {"id":"26","sap_abbreviation":"GUEBG","sap_full_text":"Gültigkeitsbeginn"},
        {"id":"27","sap_abbreviation":"GUEEN","sap_full_text":"Gültigkeitsende"},
        {"id":"28","sap_abbreviation":"KNUMV","sap_full_text":"Nr. Belegkondition"},
        {"id":"29","sap_abbreviation":"VDATU","sap_full_text":"Wunschlieferdatum"},
        {"id":"30","sap_abbreviation":"VPRGR","sap_full_text":"Periode zum Termin"},
        {"id":"31","sap_abbreviation":"AUTLF","sap_full_text":"Komplettlieferung"},
        {"id":"32","sap_abbreviation":"VBKLA","sap_full_text":"Ursprungsssystem"},
        {"id":"33","sap_abbreviation":"VBKLT","sap_full_text":"Kennzeichnung"},
        {"id":"34","sap_abbreviation":"KALSM","sap_full_text":"Kalkulationsschema"},
        {"id":"35","sap_abbreviation":"VSBED","sap_full_text":"Versandbedingung"},
        {"id":"36","sap_abbreviation":"FKARA","sap_full_text":"Auftr.bez. Fakt.Art"},
        {"id":"37","sap_abbreviation":"AWAHR","sap_full_text":"Wahrscheinlichkeit"},
        {"id":"38","sap_abbreviation":"KTEXT","sap_full_text":"Bezeichnung"},
        {"id":"39","sap_abbreviation":"BSTNK","sap_full_text":"Bestellnummer"},
        {"id":"40","sap_abbreviation":"BSARK","sap_full_text":"Bestellart"},
        {"id":"41","sap_abbreviation":"BSTDK","sap_full_text":"Bestelldatum"},
        {"id":"42","sap_abbreviation":"BSTZD","sap_full_text":"Zusatz"},
        {"id":"43","sap_abbreviation":"IHREZ","sap_full_text":"Ihr Zeichen"},
        {"id":"44","sap_abbreviation":"BNAME","sap_full_text":"Name"},
        {"id":"45","sap_abbreviation":"TELF1","sap_full_text":"Telefon"},
        {"id":"46","sap_abbreviation":"MAHZA","sap_full_text":"Anzahl Mahnungen"},
        {"id":"47","sap_abbreviation":"MAHDT","sap_full_text":"Letzte Mahnung"},
        {"id":"48","sap_abbreviation":"KUNNR","sap_full_text":"Auftraggeber"},
        {"id":"49","sap_abbreviation":"KOSTL","sap_full_text":"Kostenstelle"},
        {"id":"50","sap_abbreviation":"STAFO","sap_full_text":"FortschreibGruppe"},
        {"id":"51","sap_abbreviation":"STWAE","sap_full_text":"Statistikwährung"},
        {"id":"52","sap_abbreviation":"AEDAT","sap_full_text":"Geändert am"},
        {"id":"53","sap_abbreviation":"KVGR1","sap_full_text":"Kundengruppe 1"},
        {"id":"54","sap_abbreviation":"KVGR2","sap_full_text":"Kundengruppe 2"},
        {"id":"55","sap_abbreviation":"KVGR3","sap_full_text":"Kundengruppe 3"},
        {"id":"56","sap_abbreviation":"KVGR4","sap_full_text":"Kundengruppe 4"},
        {"id":"57","sap_abbreviation":"KVGR5","sap_full_text":"Kundengruppe 5"},
        {"id":"58","sap_abbreviation":"KNUMA","sap_full_text":"Absprache"},
        {"id":"59","sap_abbreviation":"KOKRS","sap_full_text":"Kostenrechnungskreis"},
        {"id":"60","sap_abbreviation":"PS_PSP_PNR","sap_full_text":"PSP-Element"},
        {"id":"61","sap_abbreviation":"KURST","sap_full_text":"Kurstyp"},
        {"id":"62","sap_abbreviation":"KKBER","sap_full_text":"Kreditkontr.Bereich"},
        {"id":"63","sap_abbreviation":"KNKLI","sap_full_text":"Kreditkonto"},
        {"id":"64","sap_abbreviation":"GRUPP","sap_full_text":"KundenkreditGrp"},
        {"id":"65","sap_abbreviation":"SBGRP","sap_full_text":"Bearbeitergruppe"},
        {"id":"66","sap_abbreviation":"CTLPC","sap_full_text":"Risikoklasse"},
        {"id":"67","sap_abbreviation":"CMWAE","sap_full_text":"Währung"},
        {"id":"68","sap_abbreviation":"CMFRE","sap_full_text":"Freigabedatum"},
        {"id":"69","sap_abbreviation":"CMNUP","sap_full_text":"Nächste Prüfung"},
        {"id":"70","sap_abbreviation":"CMNGV","sap_full_text":"Nächstes Datum"},
        {"id":"71","sap_abbreviation":"AMTBL","sap_full_text":"Freigegeb Kreditwert"},
        {"id":"72","sap_abbreviation":"HITYP_PR","sap_full_text":"HierTypPreisfindung"},
        {"id":"73","sap_abbreviation":"ABRVW","sap_full_text":"Verwendung"},
        {"id":"74","sap_abbreviation":"ABDIS","sap_full_text":"Dispobeh.Abrufarten"},
        {"id":"75","sap_abbreviation":"VGBEL","sap_full_text":"Vorlagebeleg"},
        {"id":"76","sap_abbreviation":"OBJNR","sap_full_text":"Objektnummer Kopf"},
        {"id":"77","sap_abbreviation":"BUKRS_VF","sap_full_text":"FaktBuchungskreis"},
        {"id":"78","sap_abbreviation":"TAXK1","sap_full_text":"Abweich.Steuerklasse"},
        {"id":"79","sap_abbreviation":"TAXK2","sap_full_text":"Steuerklassifi.2-Kd"},
        {"id":"80","sap_abbreviation":"TAXK3","sap_full_text":"Steuerklassifi.3-Kd"},
        {"id":"81","sap_abbreviation":"TAXK4","sap_full_text":"Steuerklassifi.4-Kd"},
        {"id":"82","sap_abbreviation":"TAXK5","sap_full_text":"Steuerklassifi.5-Kd"},
        {"id":"83","sap_abbreviation":"TAXK6","sap_full_text":"Steuerklassifi.6-Kd"},
        {"id":"84","sap_abbreviation":"TAXK7","sap_full_text":"Steuerklassifi.7-Kd"},
        {"id":"85","sap_abbreviation":"TAXK8","sap_full_text":"Steuerklassifi.8-Kd"},
        {"id":"86","sap_abbreviation":"TAXK9","sap_full_text":"Steuerklassifi.9-Kd"},
        {"id":"87","sap_abbreviation":"XBLNR","sap_full_text":"Referenz"},
        {"id":"88","sap_abbreviation":"ZUONR","sap_full_text":"Zuordnung"},
        {"id":"89","sap_abbreviation":"VGTYP","sap_full_text":"Vorgängerbelegtyp"},
        {"id":"90","sap_abbreviation":"KALSM_CH","sap_full_text":"Suchschema"},
        {"id":"91","sap_abbreviation":"AGRZR","sap_full_text":"Abgrenzungszeitraum"},
        {"id":"92","sap_abbreviation":"AUFNR","sap_full_text":"Auftrag"},
        {"id":"93","sap_abbreviation":"QMNUM","sap_full_text":"Meldung"},
        {"id":"94","sap_abbreviation":"VBELN_GRP","sap_full_text":"Gruppenkontrakt"},
        {"id":"95","sap_abbreviation":"SCHEME_GRP","sap_full_text":"GrpReferenzschema"},
        {"id":"96","sap_abbreviation":"ABRUF_PART","sap_full_text":"Abrufprüfung Partner"},
        {"id":"97","sap_abbreviation":"ABHOD","sap_full_text":"Abholdatum"},
        {"id":"98","sap_abbreviation":"ABHOV","sap_full_text":"Abholzeit"},
        {"id":"99","sap_abbreviation":"ABHOB","sap_full_text":"Abholzeit"},
        {"id":"100","sap_abbreviation":"RPLNR","sap_full_text":"Ratenplannummer"},
        {"id":"101","sap_abbreviation":"VZEIT","sap_full_text":"Wunschlieferuhrzeit"},
        {"id":"102","sap_abbreviation":"STCEG_L","sap_full_text":"SteuerEmpfangsland"},
        {"id":"103","sap_abbreviation":"LANDTX","sap_full_text":"SteuerAbgangsland"},
        {"id":"104","sap_abbreviation":"XEGDR","sap_full_text":"EU-Dreiecksgeschäft"},
        {"id":"105","sap_abbreviation":"ENQUEUE_GRP","sap_full_text":"Gruppenkontrakt sperren bis alle Unterkontrakte aktualisiert"},
        {"id":"106","sap_abbreviation":"DAT_FZAU","sap_full_text":"Datum AuftragsFZ"},
        {"id":"107","sap_abbreviation":"FMBDAT","sap_full_text":"Mat.Bereitst.Datum"},
        {"id":"108","sap_abbreviation":"VSNMR_V","sap_full_text":"Version"},
        {"id":"109","sap_abbreviation":"HANDLE","sap_full_text":"Handle"},
        {"id":"110","sap_abbreviation":"PROLI","sap_full_text":"GgAbwicklungsprofil"},
        {"id":"111","sap_abbreviation":"CONT_DG","sap_full_text":"Enthält Gefahrgüter"},
        {"id":"112","sap_abbreviation":"CRM_GUID","sap_full_text":"char70"},
        {"id":"113","sap_abbreviation":"UPD_TMSTMP","sap_full_text":"Zeitstempel"},
        {"id":"114","sap_abbreviation":"MSR_ID","sap_full_text":"Prozess-ID-Nummer"},
        {"id":"115","sap_abbreviation":"TM_CTRL_KEY","sap_full_text":"Steuerschlüssel"},
        {"id":"116","sap_abbreviation":"HANDOVERLOC","sap_full_text":"Übergabeort"},
        {"id":"117","sap_abbreviation":"PSM_BUDAT","sap_full_text":"Buchungsdatum"},
        {"id":"118","sap_abbreviation":"SWENR","sap_full_text":"Wirtschaftseinheit"},
        {"id":"119","sap_abbreviation":"SMENR","sap_full_text":"Einheitennummer"},
        {"id":"120","sap_abbreviation":"PHASE","sap_full_text":"Verkaufsphase"},
        {"id":"121","sap_abbreviation":"MTLAUR","sap_full_text":"Zieleinkommen"},
        {"id":"122","sap_abbreviation":"STAGE","sap_full_text":"Bauabschnitt"},
        {"id":"123","sap_abbreviation":"HB_CONT_REASON","sap_full_text":"Vorbehaltsgrund"},
        {"id":"124","sap_abbreviation":"HB_EXPDATE","sap_full_text":"Ablaufdatum"},
        {"id":"125","sap_abbreviation":"HB_RESDATE","sap_full_text":"Aufhebungsdatum"},
        {"id":"126","sap_abbreviation":"MILL_APPL_ID","sap_full_text":"Applikations-ID"},
        {"id":"127","sap_abbreviation":"LOGSYSB","sap_full_text":"Log. System Beleg"},
        {"id":"128","sap_abbreviation":"KALCD","sap_full_text":"Schema Kampagnenf."},
        {"id":"129","sap_abbreviation":"MULTI","sap_full_text":"Mehrere Promotions"},
        {"id":"130","sap_abbreviation":"SPPAYM","sap_full_text":"Zahlweg"},
        {"id":"131","sap_abbreviation":"WTYSC_CLM_HDR","sap_full_text":"Antragskopf"},
        {"id":"132","sap_abbreviation":"ZZFFPNR","sap_full_text":"MetallabsicherungsNr"},
        {"id":"133","sap_abbreviation":"ZZZOLL","sap_full_text":"Flag ohne Zoll"},
        {"id":"134","sap_abbreviation":"POSNR","sap_full_text":"Position"},
        {"id":"135","sap_abbreviation":"MATNR","sap_full_text":"Material"},
        {"id":"136","sap_abbreviation":"MATWA","sap_full_text":"Eingeg. Material"},
        {"id":"137","sap_abbreviation":"PMATN","sap_full_text":"Preismaterial"},
        {"id":"138","sap_abbreviation":"CHARG","sap_full_text":"Charge"},
        {"id":"139","sap_abbreviation":"MATKL","sap_full_text":"Warengruppe"},
        {"id":"140","sap_abbreviation":"ARKTX","sap_full_text":"Bezeichnung"},
        {"id":"141","sap_abbreviation":"PSTYV","sap_full_text":"Positionstyp"},
        {"id":"142","sap_abbreviation":"POSAR","sap_full_text":"Positionsart"},
        {"id":"143","sap_abbreviation":"LFREL","sap_full_text":"Pos lieferrelevant"},
        {"id":"144","sap_abbreviation":"FKREL","sap_full_text":"Fakturarelevanz"},
        {"id":"145","sap_abbreviation":"UEPOS","sap_full_text":"Übergeordn. Position"},
        {"id":"146","sap_abbreviation":"GRPOS","sap_full_text":"Alternativ zu Pos."},
        {"id":"147","sap_abbreviation":"ABGRU","sap_full_text":"Absagegrund"},
        {"id":"148","sap_abbreviation":"PRODH","sap_full_text":"Produkthierarchie"},
        {"id":"149","sap_abbreviation":"ZWERT","sap_full_text":"Zielwert Rahmenvertr"},
        {"id":"150","sap_abbreviation":"ZMENG","sap_full_text":"Zielmenge"},
        {"id":"151","sap_abbreviation":"ZIEME","sap_full_text":"Zielmengeneinheit"},
        {"id":"152","sap_abbreviation":"UMZIZ","sap_full_text":"Zähler Ziel -> Lager"},
        {"id":"153","sap_abbreviation":"UMZIN","sap_full_text":"Nenner Ziel -> Lager"},
        {"id":"154","sap_abbreviation":"MEINS","sap_full_text":"Basismengeneinheit"},
        {"id":"155","sap_abbreviation":"SMENG","sap_full_text":"Staffelmenge"},
        {"id":"156","sap_abbreviation":"ABLFZ","sap_full_text":"Rundungsmenge Lief."},
        {"id":"157","sap_abbreviation":"ABDAT","sap_full_text":"Abstimmdatum"},
        {"id":"158","sap_abbreviation":"ABSFZ","sap_full_text":"Abweichung absolut"},
        {"id":"159","sap_abbreviation":"POSEX","sap_full_text":"Bestellposition"},
        {"id":"160","sap_abbreviation":"KDMAT","sap_full_text":"Kundenmaterial"},
        {"id":"161","sap_abbreviation":"KBVER","sap_full_text":"Abweichung proz."},
        {"id":"162","sap_abbreviation":"KEVER","sap_full_text":"Anz.Tage Abw."},
        {"id":"163","sap_abbreviation":"VKGRU","sap_full_text":"Rep.: Klassifizierung von Positionen"},
        {"id":"164","sap_abbreviation":"VKAUS","sap_full_text":"Verwendung"},
        {"id":"165","sap_abbreviation":"GRKOR","sap_full_text":"Liefergruppe"},
        {"id":"166","sap_abbreviation":"FMENG","sap_full_text":"Menge ist fix"},
        {"id":"167","sap_abbreviation":"UEBTK","sap_full_text":"Tol. unbegrenzt"},
        {"id":"168","sap_abbreviation":"UEBTO","sap_full_text":"Tol.Überlieferung"},
        {"id":"169","sap_abbreviation":"UNTTO","sap_full_text":"Tol.Unterlieferung"},
        {"id":"170","sap_abbreviation":"FAKSP","sap_full_text":"Fakturasperre"},
        {"id":"171","sap_abbreviation":"ATPKZ","sap_full_text":"Austauschteil"},
        {"id":"172","sap_abbreviation":"RKFKF","sap_full_text":"Fakturierform RK\/PPS"},
        {"id":"173","sap_abbreviation":"ANTLF","sap_full_text":"Max.Teillieferungen"},
        {"id":"174","sap_abbreviation":"KZTLF","sap_full_text":"Teillieferung\/Pos."},
        {"id":"175","sap_abbreviation":"CHSPL","sap_full_text":"Chargensplit erlaubt"},
        {"id":"176","sap_abbreviation":"KWMENG","sap_full_text":"Auftragsmenge"},
        {"id":"177","sap_abbreviation":"LSMENG","sap_full_text":"Liefersollmenge"},
        {"id":"178","sap_abbreviation":"KBMENG","sap_full_text":"Kum.bestätigte Menge"},
        {"id":"179","sap_abbreviation":"KLMENG","sap_full_text":"Kum.bestätigte Menge"},
        {"id":"180","sap_abbreviation":"VRKME","sap_full_text":"Verkaufsmengeneinh."},
        {"id":"181","sap_abbreviation":"UMVKZ","sap_full_text":"Zaehler"},
        {"id":"182","sap_abbreviation":"UMVKN","sap_full_text":"Nenner"},
        {"id":"183","sap_abbreviation":"BRGEW","sap_full_text":"Bruttogewicht"},
        {"id":"184","sap_abbreviation":"NTGEW","sap_full_text":"Nettogewicht"},
        {"id":"185","sap_abbreviation":"GEWEI","sap_full_text":"Gewichtseinheit"},
        {"id":"186","sap_abbreviation":"VOLUM","sap_full_text":"Volumen"},
        {"id":"187","sap_abbreviation":"VOLEH","sap_full_text":"Volumeneinheit"},
        {"id":"188","sap_abbreviation":"VBELV","sap_full_text":"Verursacher"},
        {"id":"189","sap_abbreviation":"POSNV","sap_full_text":"Position"},
        {"id":"190","sap_abbreviation":"VGPOS","sap_full_text":"Vorlage Gesch. Pos."},
        {"id":"191","sap_abbreviation":"VOREF","sap_full_text":"Vollreferenz"},
        {"id":"192","sap_abbreviation":"UPFLU","sap_full_text":"Update Belegfluß"},
        {"id":"193","sap_abbreviation":"ERLRE","sap_full_text":"Erledigungsregel"},
        {"id":"194","sap_abbreviation":"LPRIO","sap_full_text":"Lieferpriorität"},
        {"id":"195","sap_abbreviation":"WERKS","sap_full_text":"Werk"},
        {"id":"196","sap_abbreviation":"LGORT","sap_full_text":"Lagerort"},
        {"id":"197","sap_abbreviation":"VSTEL","sap_full_text":"Versandstelle\/Annahmestelle"},
        {"id":"198","sap_abbreviation":"ROUTE","sap_full_text":"Route"},
        {"id":"199","sap_abbreviation":"STKEY","sap_full_text":"Herkunft Stückliste"},
        {"id":"200","sap_abbreviation":"STDAT","sap_full_text":"StichdatumStückliste"},
        {"id":"201","sap_abbreviation":"STLNR","sap_full_text":"Stückliste"},
        {"id":"202","sap_abbreviation":"STPOS","sap_full_text":"Stücklistenpositionsnummer"},
        {"id":"203","sap_abbreviation":"AWAHR","sap_full_text":"Auftr.Wahrscheinl"},
        {"id":"204","sap_abbreviation":"TAXM1","sap_full_text":"Steuerklassifikation"},
        {"id":"205","sap_abbreviation":"TAXM2","sap_full_text":"Steuerklassifikation"},
        {"id":"206","sap_abbreviation":"TAXM3","sap_full_text":"Steuerklassifikation"},
        {"id":"207","sap_abbreviation":"TAXM4","sap_full_text":"Steuerklassifikation"},
        {"id":"208","sap_abbreviation":"TAXM5","sap_full_text":"Steuerklassifikation"},
        {"id":"209","sap_abbreviation":"TAXM6","sap_full_text":"Steuerklassifikation"},
        {"id":"210","sap_abbreviation":"TAXM7","sap_full_text":"Steuerklassifikation"},
        {"id":"211","sap_abbreviation":"TAXM8","sap_full_text":"Steuerklassifikation"},
        {"id":"212","sap_abbreviation":"TAXM9","sap_full_text":"Steuerklassifikation"},
        {"id":"213","sap_abbreviation":"VBEAF","sap_full_text":"Bearbeitungszeit fix"},
        {"id":"214","sap_abbreviation":"VBEAV","sap_full_text":"Bearbeitungszeit var"},
        {"id":"215","sap_abbreviation":"VGREF","sap_full_text":"Vorgängerbeleg ist aus Referenz entst."},
        {"id":"216","sap_abbreviation":"NETPR","sap_full_text":"Nettopreis"},
        {"id":"217","sap_abbreviation":"KPEIN","sap_full_text":"Preiseinheit"},
        {"id":"218","sap_abbreviation":"KMEIN","sap_full_text":"Mengeneinheit"},
        {"id":"219","sap_abbreviation":"SHKZG","sap_full_text":"Retoure"},
        {"id":"220","sap_abbreviation":"SKTOF","sap_full_text":"Skontofähig"},
        {"id":"221","sap_abbreviation":"MTVFP","sap_full_text":"Verfügbarkeitsprüf."},
        {"id":"222","sap_abbreviation":"SUMBD","sap_full_text":"Summierung Bedarf"},
        {"id":"223","sap_abbreviation":"KONDM","sap_full_text":"Materialgruppe"},
        {"id":"224","sap_abbreviation":"KTGRM","sap_full_text":"Kontierungsgr. Mat."},
        {"id":"225","sap_abbreviation":"BONUS","sap_full_text":"Bonusgruppe"},
        {"id":"226","sap_abbreviation":"PROVG","sap_full_text":"Provisionsgruppe"},
        {"id":"227","sap_abbreviation":"EANNR","sap_full_text":"EAN-Nummer"},
        {"id":"228","sap_abbreviation":"PRSOK","sap_full_text":"Preisfindung"},
        {"id":"229","sap_abbreviation":"BWTAR","sap_full_text":"Bewertungsart"},
        {"id":"230","sap_abbreviation":"BWTEX","sap_full_text":"getrennte Bewertung"},
        {"id":"231","sap_abbreviation":"XCHPF","sap_full_text":"Chargenpflicht"},
        {"id":"232","sap_abbreviation":"XCHAR","sap_full_text":"Chargenführung"},
        {"id":"233","sap_abbreviation":"LFMNG","sap_full_text":"Mindestliefermenge"},
        {"id":"234","sap_abbreviation":"WAVWR","sap_full_text":"Verrechnungswert"},
        {"id":"235","sap_abbreviation":"KZWI1","sap_full_text":"Zwischensumme 1"},
        {"id":"236","sap_abbreviation":"KZWI2","sap_full_text":"Zwischensumme 2"},
        {"id":"237","sap_abbreviation":"KZWI3","sap_full_text":"Zwischensumme 3"},
        {"id":"238","sap_abbreviation":"KZWI4","sap_full_text":"Zwischensumme 4"},
        {"id":"239","sap_abbreviation":"KZWI5","sap_full_text":"Zwischensumme 5"},
        {"id":"240","sap_abbreviation":"KZWI6","sap_full_text":"Zwischensumme 6"},
        {"id":"241","sap_abbreviation":"STCUR","sap_full_text":"Kurs Statistken"},
        {"id":"242","sap_abbreviation":"EAN11","sap_full_text":"EAN\/UPC-Code"},
        {"id":"243","sap_abbreviation":"FIXMG","sap_full_text":"Termin u.Menge fix"},
        {"id":"244","sap_abbreviation":"PRCTR","sap_full_text":"Profitcenter"},
        {"id":"245","sap_abbreviation":"MVGR1","sap_full_text":"Materialgruppe 1"},
        {"id":"246","sap_abbreviation":"MVGR2","sap_full_text":"Materialgruppe 2"},
        {"id":"247","sap_abbreviation":"MVGR3","sap_full_text":"Materialgruppe 3"},
        {"id":"248","sap_abbreviation":"MVGR4","sap_full_text":"Materialgruppe 4"},
        {"id":"249","sap_abbreviation":"MVGR5","sap_full_text":"Materialgruppe 5"},
        {"id":"250","sap_abbreviation":"KMPMG","sap_full_text":"Komponentenmenge"},
        {"id":"251","sap_abbreviation":"SUGRD","sap_full_text":"Substitutionsgrund"},
        {"id":"252","sap_abbreviation":"SOBKZ","sap_full_text":"Sonderbestand"},
        {"id":"253","sap_abbreviation":"VPZUO","sap_full_text":"Zuordnungskennz"},
        {"id":"254","sap_abbreviation":"PAOBJNR","sap_full_text":"Ergebnisobjektnummer"},
        {"id":"255","sap_abbreviation":"VPMAT","sap_full_text":"Vorplanmaterial"},
        {"id":"256","sap_abbreviation":"VPWRK","sap_full_text":"Vorplanungswerk"},
        {"id":"257","sap_abbreviation":"PRBME","sap_full_text":"Produktgr.ME"},
        {"id":"258","sap_abbreviation":"UMREF","sap_full_text":"Umrechnung"},
        {"id":"259","sap_abbreviation":"KNTTP","sap_full_text":"Kontierungstyp"},
        {"id":"260","sap_abbreviation":"KZVBR","sap_full_text":"Verbrauch"},
        {"id":"261","sap_abbreviation":"SERNR","sap_full_text":"Seriennummer"},
        {"id":"262","sap_abbreviation":"OBJNR","sap_full_text":"Objektnr. Position"},
        {"id":"263","sap_abbreviation":"ABGRS","sap_full_text":"Abgrenzungsschlüssel"},
        {"id":"264","sap_abbreviation":"BEDAE","sap_full_text":"Bedarfsart"},
        {"id":"265","sap_abbreviation":"CMPRE","sap_full_text":"Kreditpreis"},
        {"id":"266","sap_abbreviation":"CMTFG","sap_full_text":"Teilfreigabe"},
        {"id":"267","sap_abbreviation":"CMPNT","sap_full_text":"aktive Forderung"},
        {"id":"268","sap_abbreviation":"CMKUA","sap_full_text":"Kurs Kreditdaten"},
        {"id":"269","sap_abbreviation":"CUOBJ","sap_full_text":"Konfiguration"},
        {"id":"270","sap_abbreviation":"CUOBJ_CH","sap_full_text":"Interne Objektnummer"},
        {"id":"271","sap_abbreviation":"CEPOK","sap_full_text":"ErwarteterPreis"},
        {"id":"272","sap_abbreviation":"KOUPD","sap_full_text":"Konditionsupdate"},
        {"id":"273","sap_abbreviation":"SERAIL","sap_full_text":"Serialnummernprofil"},
        {"id":"274","sap_abbreviation":"ANZSN","sap_full_text":"Anzahl Serialnummern"},
        {"id":"275","sap_abbreviation":"NACHL","sap_full_text":"kein WE beim Kunden"},
        {"id":"276","sap_abbreviation":"MAGRV","sap_full_text":"Materialgruppe PM"},
        {"id":"277","sap_abbreviation":"MPROK","sap_full_text":"ManuellerPreis"},
        {"id":"278","sap_abbreviation":"PROSA","sap_full_text":"ArtikelSel. aktiv"},
        {"id":"279","sap_abbreviation":"UEPVW","sap_full_text":"Verwendung UEPOS"},
        {"id":"280","sap_abbreviation":"KALNR","sap_full_text":"Kalkulationsnummer"},
        {"id":"281","sap_abbreviation":"KLVAR","sap_full_text":"Kalkulationsvariante"},
        {"id":"282","sap_abbreviation":"SPOSN","sap_full_text":"Positionsnr"},
        {"id":"283","sap_abbreviation":"KOWRR","sap_full_text":"Wert statistisch"},
        {"id":"284","sap_abbreviation":"STADAT","sap_full_text":"Statistikdatum"},
        {"id":"285","sap_abbreviation":"EXART","sap_full_text":"Geschäftsart"},
        {"id":"286","sap_abbreviation":"PREFE","sap_full_text":"Berecht.f.Zollverg."},
        {"id":"287","sap_abbreviation":"KNUMH","sap_full_text":"Nr. Kond.Satz Charge"},
        {"id":"288","sap_abbreviation":"CLINT","sap_full_text":"Int.Klasnr"},
        {"id":"289","sap_abbreviation":"CHMVS","sap_full_text":"Mengenvorschlag"},
        {"id":"290","sap_abbreviation":"STLTY","sap_full_text":"Stücklistentyp"},
        {"id":"291","sap_abbreviation":"STLKN","sap_full_text":"Knoten Position"},
        {"id":"292","sap_abbreviation":"STPOZ","sap_full_text":"Zähler"},
        {"id":"293","sap_abbreviation":"STMAN","sap_full_text":"Konfig. inkonsistent"},
        {"id":"294","sap_abbreviation":"ZSCHL_K","sap_full_text":"Zuschlagsschlüssel"},
        {"id":"295","sap_abbreviation":"KALSM_K","sap_full_text":"Kalkulationsschema"},
        {"id":"296","sap_abbreviation":"KALVAR","sap_full_text":"Kalkulationsvariante"},
        {"id":"297","sap_abbreviation":"KOSCH","sap_full_text":"KontingentSchema"},
        {"id":"298","sap_abbreviation":"UPMAT","sap_full_text":"PreisMat HauptPositn"},
        {"id":"299","sap_abbreviation":"UKONM","sap_full_text":"MaterialGr HauptPos"},
        {"id":"300","sap_abbreviation":"MFRGR","sap_full_text":"MatFraGruppe"},
        {"id":"301","sap_abbreviation":"PLAVO","sap_full_text":"Planabrufvorschrift"},
        {"id":"302","sap_abbreviation":"KANNR","sap_full_text":"Sequenz-Nummer"},
        {"id":"303","sap_abbreviation":"CMPRE_FLT","sap_full_text":"Kreditpreis"},
        {"id":"304","sap_abbreviation":"ABFOR","sap_full_text":"Absicherungsform"},
        {"id":"305","sap_abbreviation":"ABGES","sap_full_text":"abgesichert"},
        {"id":"306","sap_abbreviation":"J_1BCFOP","sap_full_text":"CFOP"},
        {"id":"307","sap_abbreviation":"J_1BTAXLW1","sap_full_text":"Gesetz ICMS"},
        {"id":"308","sap_abbreviation":"J_1BTAXLW2","sap_full_text":"Gesetz IPI"},
        {"id":"309","sap_abbreviation":"J_1BTXSDC","sap_full_text":"Steuerkennzeichen"},
        {"id":"310","sap_abbreviation":"WKTNR","sap_full_text":"Wertkontraktnummer"},
        {"id":"311","sap_abbreviation":"WKTPS","sap_full_text":"Wertkontraktposition"},
        {"id":"312","sap_abbreviation":"SKOPF","sap_full_text":"Baustein"},
        {"id":"313","sap_abbreviation":"KZBWS","sap_full_text":"Bewertung SondBest"},
        {"id":"314","sap_abbreviation":"WGRU1","sap_full_text":"Warengruppe 1"},
        {"id":"315","sap_abbreviation":"WGRU2","sap_full_text":"Warengruppe 2"},
        {"id":"316","sap_abbreviation":"KNUMA_PI","sap_full_text":"Promotion"},
        {"id":"317","sap_abbreviation":"KNUMA_AG","sap_full_text":"Verkaufsaktion"},
        {"id":"318","sap_abbreviation":"KZFME","sap_full_text":"Führende Mengeneinh."},
        {"id":"319","sap_abbreviation":"LSTANR","sap_full_text":"Liefersteuerung Naturalrabatt"},
        {"id":"320","sap_abbreviation":"TECHS","sap_full_text":"Standardbewertung"},
        {"id":"321","sap_abbreviation":"MWSBP","sap_full_text":"Steuerbetrag"},
        {"id":"322","sap_abbreviation":"BERID","sap_full_text":"Dispobereich"},
        {"id":"323","sap_abbreviation":"PCTRF","sap_full_text":"Profit Center Faktur"},
        {"id":"324","sap_abbreviation":"LOGSYS_EXT","sap_full_text":"Logisches System"},
        {"id":"325","sap_abbreviation":"J_1BTAXLW3","sap_full_text":"ISS-Gesetz"},
        {"id":"326","sap_abbreviation":"J_1BTAXLW4","sap_full_text":"COFINS Gesetz"},
        {"id":"327","sap_abbreviation":"J_1BTAXLW5","sap_full_text":"PIS-Gesetz"},
        {"id":"328","sap_abbreviation":"STOCKLOC","sap_full_text":"Lokation"},
        {"id":"329","sap_abbreviation":"SLOCTYPE","sap_full_text":"Lokationstyp"},
        {"id":"330","sap_abbreviation":"MSR_RET_REASON","sap_full_text":"Retourengrund"},
        {"id":"331","sap_abbreviation":"MSR_REFUND_CODE","sap_full_text":"RückerstattSchlü."},
        {"id":"332","sap_abbreviation":"MSR_APPROV_BLOCK","sap_full_text":"Genehmigung"},
        {"id":"333","sap_abbreviation":"NRAB_KNUMH","sap_full_text":"Nr. Konditionssatz"},
        {"id":"334","sap_abbreviation":"TRMRISK_RELEVANT","sap_full_text":"Risikorelevanz"},
        {"id":"335","sap_abbreviation":"SGT_RCAT","sap_full_text":"Bedarfssegment"},
        {"id":"336","sap_abbreviation":"HANDOVERDATE","sap_full_text":"Übergabedatum"},
        {"id":"337","sap_abbreviation":"HANDOVERTIME","sap_full_text":"Übergabezeit"},
        {"id":"338","sap_abbreviation":"TC_AUT_DET","sap_full_text":"Steuerkennzeichen automatisch ermittelt"},
        {"id":"339","sap_abbreviation":"MANUAL_TC_REASON","sap_full_text":"Grund für manuelles Steuerkennzeichen"},
        {"id":"340","sap_abbreviation":"FISCAL_INCENTIVE","sap_full_text":"Art des steuerlichen Anreizes"},
        {"id":"341","sap_abbreviation":"TAX_SUBJECT_ST","sap_full_text":"Steuerpflicht (Substituicao Tributaria)"},
        {"id":"342","sap_abbreviation":"FISCAL_INCENTIVE_ID","sap_full_text":"Anreiz-ID"},
        {"id":"343","sap_abbreviation":"SPCSTO","sap_full_text":"NF CFOP Sonderfall"},
        {"id":"344","sap_abbreviation":"REVACC_REFID","sap_full_text":"Erlösbuchhaltung: Ref.-ID"},
        {"id":"345","sap_abbreviation":"REVACC_REFTYPE","sap_full_text":"ErlösbuchhaltReferenztyp"},
        {"id":"346","sap_abbreviation":"SESSION_CREATION_DATE","sap_full_text":"Session angelegt am"},
        {"id":"347","sap_abbreviation":"SESSION_CREATION_TIME","sap_full_text":"Session angelegt um"},
        {"id":"348","sap_abbreviation":"\/BEV1\/SRFUND","sap_full_text":"Analyse\/Absagegrund"},
        {"id":"349","sap_abbreviation":"AUFPL_OLC","sap_full_text":"Plannummer Vorgänge"},
        {"id":"350","sap_abbreviation":"APLZL_OLC","sap_full_text":"Zähler"},
        {"id":"351","sap_abbreviation":"FERC_IND","sap_full_text":"Kz. Meldewesen"},
        {"id":"352","sap_abbreviation":"FONDS","sap_full_text":"Fonds"},
        {"id":"353","sap_abbreviation":"FISTL","sap_full_text":"Finanzstelle"},
        {"id":"354","sap_abbreviation":"FKBER","sap_full_text":"Funktionsbereich"},
        {"id":"355","sap_abbreviation":"GRANT_NBR","sap_full_text":"Förderung"},
        {"id":"356","sap_abbreviation":"IUID_RELEVANT","sap_full_text":"IUID-relevant für Kunde"},
        {"id":"357","sap_abbreviation":"MILL_SE_GPOSN","sap_full_text":"globale Position"},
        {"id":"358","sap_abbreviation":"PRS_OBJNR","sap_full_text":"Auftragsabwicklung: Objektnummer"},
        {"id":"359","sap_abbreviation":"PRS_SD_SPSNR","sap_full_text":"Standard-PSP-Element"},
        {"id":"360","sap_abbreviation":"PRS_WORK_PERIOD","sap_full_text":"Leistungsperiode"},
        {"id":"361","sap_abbreviation":"PARGB","sap_full_text":"PartnerGsber"},
        {"id":"362","sap_abbreviation":"AUFPL_OAA","sap_full_text":"Plannummer Vorgänge"},
        {"id":"363","sap_abbreviation":"APLZL_OAA","sap_full_text":"Zähler"},
        {"id":"364","sap_abbreviation":"ARSNUM","sap_full_text":"Reservierung"},
        {"id":"365","sap_abbreviation":"ARSPOS","sap_full_text":"Pos.-Nr. der Reservierung"},
        {"id":"366","sap_abbreviation":"WTYSC_CLMITEM","sap_full_text":"Antragspositionsnummer"},
        {"id":"367","sap_abbreviation":"ZZQMNUM","sap_full_text":"Meldung"},
        {"id":"368","sap_abbreviation":"ZZPRGBZ","sap_full_text":"Lieferdatum"},
        {"id":"369","sap_abbreviation":"ZZETDAT","sap_full_text":"Lieferdatum"},
        {"id":"370","sap_abbreviation":"\/WSW\/SPEEDI_F1","sap_full_text":"Datum"},
        {"id":"371","sap_abbreviation":"\/WSW\/SPEEDI_F2","sap_full_text":"Character Länge 1"},
        {"id":"372","sap_abbreviation":"\/WSW\/SPEEDI_F3","sap_full_text":"Character Länge 1"},
        {"id":"373","sap_abbreviation":"\/WSW\/SPEEDI_F4","sap_full_text":"Character Länge 1"},
        {"id":"374","sap_abbreviation":"\/WSW\/SPEEDI_F5","sap_full_text":"Character Länge 1"},
        {"id":"375","sap_abbreviation":"ZZCM2PST","sap_full_text":"m2 pro Stück"},
        {"id":"376","sap_abbreviation":"ZZCALU_F","sap_full_text":"Alufaktor"},
        {"id":"377","sap_abbreviation":"ZZCM2GES","sap_full_text":"m² pro Pos"},
        {"id":"378","sap_abbreviation":"VBELN","sap_full_text":"Vertriebsbeleg"},
        {"id":"379","sap_abbreviation":"POSNR","sap_full_text":"Position (SD)"},
        {"id":"380","sap_abbreviation":"KONDA","sap_full_text":"Preisgruppe"},
        {"id":"381","sap_abbreviation":"KDGRP","sap_full_text":"Kundengruppe"},
        {"id":"382","sap_abbreviation":"BZIRK","sap_full_text":"Kundenbezirk"},
        {"id":"383","sap_abbreviation":"PLTYP","sap_full_text":"Preisliste"},
        {"id":"384","sap_abbreviation":"INCO1","sap_full_text":"Incoterms"},
        {"id":"385","sap_abbreviation":"INCO2","sap_full_text":"Incoterms Teil 2"},
        {"id":"386","sap_abbreviation":"KZAZU","sap_full_text":"AuftrZusammenführung"},
        {"id":"387","sap_abbreviation":"PERFK","sap_full_text":"Rechnungstermine"},
        {"id":"388","sap_abbreviation":"PERRL","sap_full_text":"RechListenTermine"},
        {"id":"389","sap_abbreviation":"MRNKZ","sap_full_text":"Rechnungsnachbearb."},
        {"id":"390","sap_abbreviation":"KURRF","sap_full_text":"Kurs f.Buchhaltung"},
        {"id":"391","sap_abbreviation":"VALTG","sap_full_text":"Zusätzl. Valutatage"},
        {"id":"392","sap_abbreviation":"VALDT","sap_full_text":"Valuta-Fixdatum"},
        {"id":"393","sap_abbreviation":"ZTERM","sap_full_text":"Zahlungsbedingung"},
        {"id":"394","sap_abbreviation":"ZLSCH","sap_full_text":"Zahlweg"},
        {"id":"395","sap_abbreviation":"KTGRD","sap_full_text":"Kontierungsgr. Deb."},
        {"id":"396","sap_abbreviation":"KURSK","sap_full_text":"Kurs"},
        {"id":"397","sap_abbreviation":"PRSDT","sap_full_text":"Preisdatum"},
        {"id":"398","sap_abbreviation":"FKDAT","sap_full_text":"Fakturadatum"},
        {"id":"399","sap_abbreviation":"FBUDA","sap_full_text":"Leistungserst.Dat"},
        {"id":"400","sap_abbreviation":"GJAHR","sap_full_text":"Geschäftsjahr"},
        {"id":"401","sap_abbreviation":"POPER","sap_full_text":"Buchungsperiode"},
        {"id":"402","sap_abbreviation":"STCUR","sap_full_text":"Kurs Statistiken"},
        {"id":"403","sap_abbreviation":"MSCHL","sap_full_text":"Mahnschlüssel"},
        {"id":"404","sap_abbreviation":"MANSP","sap_full_text":"Mahnsperre"},
        {"id":"405","sap_abbreviation":"FPLNR","sap_full_text":"Fakturierungsplannummer"},
        {"id":"406","sap_abbreviation":"WAKTION","sap_full_text":"Aktion"},
        {"id":"407","sap_abbreviation":"ABSSC","sap_full_text":"Absicherungsschema"},
        {"id":"408","sap_abbreviation":"LCNUM","sap_full_text":"Finanzdokumentnummer"},
        {"id":"409","sap_abbreviation":"J_1AFITP","sap_full_text":"Steuerart"},
        {"id":"410","sap_abbreviation":"J_1ARFZ","sap_full_text":"Grund 0 MwSt."},
        {"id":"411","sap_abbreviation":"J_1AREGIO","sap_full_text":"Region"},
        {"id":"412","sap_abbreviation":"J_1AGICD","sap_full_text":"Tätigkeit BE-Steuer"},
        {"id":"413","sap_abbreviation":"J_1ADTYP","sap_full_text":"Verteilungsart"},
        {"id":"414","sap_abbreviation":"J_1ATXREL","sap_full_text":"Steuerrel.Klass"},
        {"id":"415","sap_abbreviation":"ABTNR","sap_full_text":"Abteilung"},
        {"id":"416","sap_abbreviation":"EMPST","sap_full_text":"Empfangsstelle"},
        {"id":"417","sap_abbreviation":"BSTKD","sap_full_text":"Bestellnummer"},
        {"id":"418","sap_abbreviation":"BSTKD_E","sap_full_text":"Bestellnummer"},
        {"id":"419","sap_abbreviation":"BSTDK_E","sap_full_text":"Bestelldatum"},
        {"id":"420","sap_abbreviation":"BSARK_E","sap_full_text":"Bestellart"},
        {"id":"421","sap_abbreviation":"IHREZ_E","sap_full_text":"Ihr Zeichen"},
        {"id":"422","sap_abbreviation":"POSEX_E","sap_full_text":"Bestellpositionsnr."},
        {"id":"423","sap_abbreviation":"KURSK_DAT","sap_full_text":"Umrechnungsdatum"},
        {"id":"424","sap_abbreviation":"KURRF_DAT","sap_full_text":"Umrechnungsdatum"},
        {"id":"425","sap_abbreviation":"KDKG1","sap_full_text":"Konditionsgruppe 1"},
        {"id":"426","sap_abbreviation":"KDKG2","sap_full_text":"Konditionsgruppe 2"},
        {"id":"427","sap_abbreviation":"KDKG3","sap_full_text":"Konditionsgruppe 3"},
        {"id":"428","sap_abbreviation":"KDKG4","sap_full_text":"Konditionsgruppe 4"},
        {"id":"429","sap_abbreviation":"KDKG5","sap_full_text":"Konditionsgruppe 5"},
        {"id":"430","sap_abbreviation":"WKWAE","sap_full_text":"Währung des zugeordneten Wertkontraktes"},
        {"id":"431","sap_abbreviation":"WKKUR","sap_full_text":"Kurs"},
        {"id":"432","sap_abbreviation":"AKWAE","sap_full_text":"Akkreditivwährung"},
        {"id":"433","sap_abbreviation":"AKKUR","sap_full_text":"Umr.kurs Akkreditiv"},
        {"id":"434","sap_abbreviation":"AKPRZ","sap_full_text":"Abschreibungsgrad"},
        {"id":"435","sap_abbreviation":"J_1AINDXP","sap_full_text":"Inflationsindex"},
        {"id":"436","sap_abbreviation":"J_1AIDATEP","sap_full_text":"Basisdat.Indizier."},
        {"id":"437","sap_abbreviation":"BSTKD_M","sap_full_text":"Bestellnummer"},
        {"id":"438","sap_abbreviation":"DELCO","sap_full_text":"Lieferzeit"},
        {"id":"439","sap_abbreviation":"FFPRF","sap_full_text":"DPP-Profil"},
        {"id":"440","sap_abbreviation":"BEMOT","sap_full_text":"Berechnungsmotiv"},
        {"id":"441","sap_abbreviation":"FAKTF","sap_full_text":"Fakturierform"},
        {"id":"442","sap_abbreviation":"RRREL","sap_full_text":"Erlösrealisierungstyp"},
        {"id":"443","sap_abbreviation":"ACDATV","sap_full_text":"Regel f. AbgrenzBeginndatum"},
        {"id":"444","sap_abbreviation":"VSART","sap_full_text":"Versandart"},
        {"id":"445","sap_abbreviation":"TRATY","sap_full_text":"Transportmittelart"},
        {"id":"446","sap_abbreviation":"TRMTYP","sap_full_text":"Transportmittel"},
        {"id":"447","sap_abbreviation":"SDABW","sap_full_text":"Sonderabwicklungskennz."},
        {"id":"448","sap_abbreviation":"WMINR","sap_full_text":"Katalog"},
        {"id":"449","sap_abbreviation":"PODKZ","sap_full_text":"LEB relevant"},
        {"id":"450","sap_abbreviation":"CAMPAIGN","sap_full_text":"CGPL_GUID"},
        {"id":"451","sap_abbreviation":"VKONT","sap_full_text":"Vertragskonto"},
        {"id":"452","sap_abbreviation":"DPBP_REF_FPLNR","sap_full_text":"Fakturierungsplannummer"},
        {"id":"453","sap_abbreviation":"DPBP_REF_FPLTR","sap_full_text":"Position"},
        {"id":"454","sap_abbreviation":"REVSP","sap_full_text":"Erlösverteilungstyp"},
        {"id":"455","sap_abbreviation":"REVEVTYP","sap_full_text":"Erlösereignistyp"},
        {"id":"456","sap_abbreviation":"FARR_RELTYPE","sap_full_text":"Erlösbuchhaltungsart"},
        {"id":"457","sap_abbreviation":"VTREF","sap_full_text":"Vertrag"},
        {"id":"458","sap_abbreviation":"_DATAAGING","sap_full_text":"Datenfilterwert für Data Aging"},
        {"id":"459","sap_abbreviation":"J_1TPBUPL","sap_full_text":""},
        {"id":"460","sap_abbreviation":"INCOV","sap_full_text":"Incoterm-Version"},
        {"id":"461","sap_abbreviation":"INCO2_L","sap_full_text":"Incoterms Standort 1"},
        {"id":"462","sap_abbreviation":"INCO3_L","sap_full_text":"Incoterms Standort 2"},
        {"id":"463","sap_abbreviation":"PEROP_BEG","sap_full_text":""},
        {"id":"464","sap_abbreviation":"PEROP_END","sap_full_text":""},
        {"id":"465","sap_abbreviation":"STCODE","sap_full_text":""},
        {"id":"466","sap_abbreviation":"FORMC1","sap_full_text":""},
        {"id":"467","sap_abbreviation":"FORMC2","sap_full_text":""},
        {"id":"468","sap_abbreviation":"STEUC","sap_full_text":"Steuerungscode"},
        {"id":"469","sap_abbreviation":"COMPREAS","sap_full_text":"Abkürzung Reklamationsgrund"},
        {"id":"470","sap_abbreviation":"MNDID","sap_full_text":"Mandatsreferenz"},
        {"id":"471","sap_abbreviation":"PAY_TYPE","sap_full_text":"Zahlungsart"},
        {"id":"472","sap_abbreviation":"SEPON","sap_full_text":"SEPA-relevant"},
        {"id":"473","sap_abbreviation":"MNDVG","sap_full_text":"SEPA-relevant"},
        {"id":"474","sap_abbreviation":"ABRLI","sap_full_text":"Interner Lieferabruf"},
        {"id":"475","sap_abbreviation":"ABART","sap_full_text":"Abrufart"},
        {"id":"476","sap_abbreviation":"DOCNUM","sap_full_text":"IDoc-Nummer"},
        {"id":"477","sap_abbreviation":"ABEFZ","sap_full_text":"Eingangs-FZ"},
        {"id":"478","sap_abbreviation":"ABRAB","sap_full_text":"Abruf gültig ab"},
        {"id":"479","sap_abbreviation":"ABRBI","sap_full_text":"Abruf gültig bis"},
        {"id":"480","sap_abbreviation":"LABNK","sap_full_text":"Abruf"},
        {"id":"481","sap_abbreviation":"ABRDT","sap_full_text":"Abrufdatum"},
        {"id":"482","sap_abbreviation":"TERSL","sap_full_text":"Terminschlüssel"},
        {"id":"483","sap_abbreviation":"LFDKD","sap_full_text":"Datum letzte Lief."},
        {"id":"484","sap_abbreviation":"LFNKD","sap_full_text":"Letzte Lieferung"},
        {"id":"485","sap_abbreviation":"ABFDA","sap_full_text":"Fert.freig.Anfang"},
        {"id":"486","sap_abbreviation":"ABFDE","sap_full_text":"Fertigungsfr. Ende"},
        {"id":"487","sap_abbreviation":"ABMDA","sap_full_text":"Materialfr. Anfang"},
        {"id":"488","sap_abbreviation":"ABMDE","sap_full_text":"Materialfr. Ende"},
        {"id":"489","sap_abbreviation":"ABLLI","sap_full_text":"Letzter Abruf"},
        {"id":"490","sap_abbreviation":"HIFFZ","sap_full_text":"Höchste FFZ"},
        {"id":"491","sap_abbreviation":"HIFFZLI","sap_full_text":"Abruf höchste FFZ"},
        {"id":"492","sap_abbreviation":"HIMFZ","sap_full_text":"Höchste MFZ"},
        {"id":"493","sap_abbreviation":"HIMFZLI","sap_full_text":"Abruf höchste MFZ"},
        {"id":"494","sap_abbreviation":"ERZEI","sap_full_text":"Uhrzeit"},
        {"id":"495","sap_abbreviation":"HILFZ","sap_full_text":"Höchste LFFZ"},
        {"id":"496","sap_abbreviation":"HILFZLI","sap_full_text":"Abruf höchste LFFZ"},
        {"id":"497","sap_abbreviation":"ABHOR","sap_full_text":"Feinabrufhorizont"},
        {"id":"498","sap_abbreviation":"GJKUN","sap_full_text":"Gs.jahr des Kunden"},
        {"id":"499","sap_abbreviation":"VJKUN","sap_full_text":"Vorjahr des Kunden"},
        {"id":"500","sap_abbreviation":"AKMFZ","sap_full_text":"Aktuelle MFZ"},
        {"id":"501","sap_abbreviation":"AKFFZ","sap_full_text":"Aktuelle FFZ"},
        {"id":"502","sap_abbreviation":"AKLFZ","sap_full_text":"Akt.Lief.Freig.FZ"},
        {"id":"503","sap_abbreviation":"KRITB","sap_full_text":"Kritischer Bestand"},
        {"id":"504","sap_abbreviation":"LABKY","sap_full_text":"Bed.Status Schlüssel"},
        {"id":"505","sap_abbreviation":"VBRST","sap_full_text":"Verbrauchsstelle"},
        {"id":"506","sap_abbreviation":"EDLLS","sap_full_text":"EDL-Entnahme"},
        {"id":"507","sap_abbreviation":"EDLDT","sap_full_text":"EDL-Datum"},
        {"id":"508","sap_abbreviation":"LFMKD","sap_full_text":"Letzte_Lief.Menge"},
        {"id":"509","sap_abbreviation":"USR01","sap_full_text":"Daten 1"},
        {"id":"510","sap_abbreviation":"USR02","sap_full_text":"Daten 2"},
        {"id":"511","sap_abbreviation":"USR03","sap_full_text":"Daten 3"},
        {"id":"512","sap_abbreviation":"USR04","sap_full_text":"Daten 4"},
        {"id":"513","sap_abbreviation":"USR05","sap_full_text":"Daten 5"},
        {"id":"514","sap_abbreviation":"CYEFZ","sap_full_text":"FZ bei Nullstellung"},
        {"id":"515","sap_abbreviation":"CYDAT","sap_full_text":"Datum Nullst. EFZ"},
        {"id":"516","sap_abbreviation":"MFLAUF","sap_full_text":"Mat.frg.Laufzeit"},
        {"id":"517","sap_abbreviation":"MFEIN","sap_full_text":"Materialfrg.Einheit"},
        {"id":"518","sap_abbreviation":"FFLAUF","sap_full_text":"Fert.frg.Laufzeit"},
        {"id":"519","sap_abbreviation":"FFEIN","sap_full_text":"Fert.frg.Einheit"},
        {"id":"520","sap_abbreviation":"ABRDT_ORG","sap_full_text":"Abrufdatum"},
        {"id":"521","sap_abbreviation":"LFMAIS","sap_full_text":"Pick-Up-Sheet"},
        {"id":"522","sap_abbreviation":"MAIDT","sap_full_text":"PUS-Datum"},
        {"id":"523","sap_abbreviation":"\/WSW\/SPEEDI_F1","sap_full_text":"Charakterfeld Länge 50"},
        {"id":"524","sap_abbreviation":"RFSTK","sap_full_text":"Referenzstatus"},
        {"id":"525","sap_abbreviation":"RFGSK","sap_full_text":"Gesamtreferenzstatus"},
        {"id":"526","sap_abbreviation":"BESTK","sap_full_text":"bestätigt"},
        {"id":"527","sap_abbreviation":"LFSTK","sap_full_text":"Lieferstatus"},
        {"id":"528","sap_abbreviation":"LFGSK","sap_full_text":"Gesamtlieferstatus"},
        {"id":"529","sap_abbreviation":"WBSTK","sap_full_text":"GesWarenbewegungStat"},
        {"id":"530","sap_abbreviation":"FKSTK","sap_full_text":"Fakturastatus"},
        {"id":"531","sap_abbreviation":"FKSAK","sap_full_text":"Fakt.Stat.auftragsb."},
        {"id":"532","sap_abbreviation":"BUCHK","sap_full_text":"Buchungsstatus"},
        {"id":"533","sap_abbreviation":"ABSTK","sap_full_text":"Absagestatus"},
        {"id":"534","sap_abbreviation":"GBSTK","sap_full_text":"Gesamtstatus"},
        {"id":"535","sap_abbreviation":"KOSTK","sap_full_text":"Gesamtstat. Kommiss."},
        {"id":"536","sap_abbreviation":"LVSTK","sap_full_text":"Gesamtstatus WM-Akt."},
        {"id":"537","sap_abbreviation":"UVALS","sap_full_text":"Positionsdaten"},
        {"id":"538","sap_abbreviation":"UVVLS","sap_full_text":"Pos.daten Lieferung"},
        {"id":"539","sap_abbreviation":"UVFAS","sap_full_text":"Pos.Dat.Faktura"},
        {"id":"540","sap_abbreviation":"UVALL","sap_full_text":"Kopfdaten"},
        {"id":"541","sap_abbreviation":"UVVLK","sap_full_text":"Kopfdaten Lieferung"},
        {"id":"542","sap_abbreviation":"UVFAK","sap_full_text":"Kopfdaten Faktura"},
        {"id":"543","sap_abbreviation":"UVPRS","sap_full_text":"Preisfindung"},
        {"id":"544","sap_abbreviation":"VBOBJ","sap_full_text":"Vertriebsbelegobjekt"},
        {"id":"545","sap_abbreviation":"FKIVK","sap_full_text":"SummenstatusIV"},
        {"id":"546","sap_abbreviation":"RELIK","sap_full_text":"RechListStatus"},
        {"id":"547","sap_abbreviation":"UVK01","sap_full_text":"Kopfreserve1"},
        {"id":"548","sap_abbreviation":"UVK02","sap_full_text":"Kopfreserve2"},
        {"id":"549","sap_abbreviation":"UVK03","sap_full_text":"Kopfreserve3"},
        {"id":"550","sap_abbreviation":"UVK04","sap_full_text":"Kopfreserve4"},
        {"id":"551","sap_abbreviation":"UVK05","sap_full_text":"Kopfreserve5"},
        {"id":"552","sap_abbreviation":"UVS01","sap_full_text":"GesamtReserve1"},
        {"id":"553","sap_abbreviation":"UVS02","sap_full_text":"GesamtReserve2"},
        {"id":"554","sap_abbreviation":"UVS03","sap_full_text":"GesamtReserve3"},
        {"id":"555","sap_abbreviation":"UVS04","sap_full_text":"GesamtReserve4"},
        {"id":"556","sap_abbreviation":"UVS05","sap_full_text":"GesamtReserve5"},
        {"id":"557","sap_abbreviation":"PKSTK","sap_full_text":"Packstatus"},
        {"id":"558","sap_abbreviation":"CMPSA","sap_full_text":"Statische Prüfung"},
        {"id":"559","sap_abbreviation":"CMPSB","sap_full_text":"Dynamische Prüfung"},
        {"id":"560","sap_abbreviation":"CMPSC","sap_full_text":"Maximaler Wert"},
        {"id":"561","sap_abbreviation":"CMPSD","sap_full_text":"Zahlungsbedingung"},
        {"id":"562","sap_abbreviation":"CMPSE","sap_full_text":"Reviewdatum Kunde"},
        {"id":"563","sap_abbreviation":"CMPSF","sap_full_text":"Überf. offene Posten"},
        {"id":"564","sap_abbreviation":"CMPSG","sap_full_text":"Ältes. offene Posten"},
        {"id":"565","sap_abbreviation":"CMPSH","sap_full_text":"Maximale Mahnstufe"},
        {"id":"566","sap_abbreviation":"CMPSI","sap_full_text":"Finanzdokument"},
        {"id":"567","sap_abbreviation":"CMPSJ","sap_full_text":"Warenkreditversichng"},
        {"id":"568","sap_abbreviation":"CMPSK","sap_full_text":"Zahlungskarte"},
        {"id":"569","sap_abbreviation":"CMPSL","sap_full_text":"Reserve"},
        {"id":"570","sap_abbreviation":"CMPS0","sap_full_text":"Reserve"},
        {"id":"571","sap_abbreviation":"CMPS1","sap_full_text":"Reserve"},
        {"id":"572","sap_abbreviation":"CMPS2","sap_full_text":"Reserve"},
        {"id":"573","sap_abbreviation":"CMGST","sap_full_text":"Gesamtstatus Kredit"},
        {"id":"574","sap_abbreviation":"TRSTA","sap_full_text":"TransportDispoStat"},
        {"id":"575","sap_abbreviation":"KOQUK","sap_full_text":"Quittierung Kommiss."},
        {"id":"576","sap_abbreviation":"COSTA","sap_full_text":"Bestellbestätigung"},
        {"id":"577","sap_abbreviation":"SAPRL","sap_full_text":"SAP-Release"},
        {"id":"578","sap_abbreviation":"UVPAS","sap_full_text":"Pos.daten Verpacken"},
        {"id":"579","sap_abbreviation":"UVPIS","sap_full_text":"Pos.daten Kommiss.\/Einl."},
        {"id":"580","sap_abbreviation":"UVWAS","sap_full_text":"Pos.daten Warenbeweg."},
        {"id":"581","sap_abbreviation":"UVPAK","sap_full_text":"Kopfdaten Verpacken"},
        {"id":"582","sap_abbreviation":"UVPIK","sap_full_text":"Kopfdaten Kommiss.\/Einlagern"},
        {"id":"583","sap_abbreviation":"UVWAK","sap_full_text":"Kopfdaten Warenbewegung"},
        {"id":"584","sap_abbreviation":"UVGEK","sap_full_text":"Kopfdaten Gefahrgut"},
        {"id":"585","sap_abbreviation":"CMPSM","sap_full_text":"Alter Kreditvektor"},
        {"id":"586","sap_abbreviation":"DCSTK","sap_full_text":"Verzugstatus"},
        {"id":"587","sap_abbreviation":"VESTK","sap_full_text":"HU eingelagert"},
        {"id":"588","sap_abbreviation":"VLSTK","sap_full_text":"Status dez. Lager"},
        {"id":"589","sap_abbreviation":"RRSTA","sap_full_text":"Erlösermittlg.status"},
        {"id":"590","sap_abbreviation":"BLOCK","sap_full_text":"Kennzeichen: Beleg für Archivierung vorgemerkt"},
        {"id":"591","sap_abbreviation":"FSSTK","sap_full_text":"G.Fakturasperrstatus"},
        {"id":"592","sap_abbreviation":"LSSTK","sap_full_text":"G.Liefersperrestatus"},
        {"id":"593","sap_abbreviation":"SPSTG","sap_full_text":"Gesamtsperrstatus"},
        {"id":"594","sap_abbreviation":"PDSTK","sap_full_text":"Lieferempf.best. Status"},
        {"id":"595","sap_abbreviation":"FMSTK","sap_full_text":"Status Funds Management"},
        {"id":"596","sap_abbreviation":"MANEK","sap_full_text":"Manuelle Erledigung des Kontraktes"},
        {"id":"597","sap_abbreviation":"SPE_TMPID","sap_full_text":"Temp. Anl."},
        {"id":"598","sap_abbreviation":"HDALL","sap_full_text":"Gemerkt"},
        {"id":"599","sap_abbreviation":"HDALS","sap_full_text":"Pos.zurück"},
        {"id":"600","sap_abbreviation":"CMPS_CM","sap_full_text":"SAP Credit Management"},
        {"id":"601","sap_abbreviation":"CMPS_TE","sap_full_text":"CM Status techn. Fehler"},
        {"id":"602","sap_abbreviation":"VBTYP_EXT","sap_full_text":"Belegtyperweiterung"},
        {"id":"603","sap_abbreviation":"KPOSN","sap_full_text":"Konditionspositionsnummer"},
        {"id":"604","sap_abbreviation":"STUNR","sap_full_text":"Stufennummer"},
        {"id":"605","sap_abbreviation":"ZAEHK","sap_full_text":"Zähler Konditionen"},
        {"id":"606","sap_abbreviation":"STUNR","sap_full_text":"Stufennummer"},
        {"id":"607","sap_abbreviation":"KSCHL","sap_full_text":"Konditionsart"},
        {"id":"608","sap_abbreviation":"KBETR","sap_full_text":"Konditionsbetrag oder -prozentsatz"},
        {"id":"609","sap_abbreviation":"WAERS","sap_full_text":"Währungsschlüssel"},
        {"id":"610","sap_abbreviation":"KPEIN","sap_full_text":"Konditions-Preiseinheit"},
        {"id":"611","sap_abbreviation":"KMEIN","sap_full_text":"Mengeneinheit Kondition im Beleg"}
]
    
    for sap_abbreviation_dictionary in sap_abbreviation_dictionary_list:
        sap_abbreviation_dictionary = SapAbbreviationDictionary(
            **sap_abbreviation_dictionary
        )
        sap_abbreviation_dictionary.save()

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