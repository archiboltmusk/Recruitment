import json
from typing import List, Dict, Any

EXAMS_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "upsc-cms-paper-1",
        "title": "UPSC Combined Medical Services (CMS) — Paper 1",
        "subtitle": "General Medicine (96 Qs) & Pediatrics (24 Qs)",
        "total_questions": 12,
        "total_marks": 250,
        "duration_minutes": 120,
        "negative_marking": 0.33,
        "subjects": ["General Medicine", "Pediatrics"],
        "year": "2024 Official Pattern",
        "difficulty": "Medium to High (Clinical Scenarios)",
        "cutoff_reference": 128
    },
    {
        "id": "upsc-cms-paper-2",
        "title": "UPSC Combined Medical Services (CMS) — Paper 2",
        "subtitle": "Surgery (40 Qs), OBG (40 Qs), and PSM (40 Qs)",
        "total_questions": 12,
        "total_marks": 250,
        "duration_minutes": 120,
        "negative_marking": 0.33,
        "subjects": ["General Surgery", "Obstetrics & Gynaecology", "Preventive & Social Medicine"],
        "year": "2024 Official Pattern",
        "difficulty": "Medium to High",
        "cutoff_reference": 132
    },
    {
        "id": "cms-clinical-pharma",
        "title": "Clinical Pharmacology & Antimicrobial Stewardship Drill",
        "subtitle": "High-Yield Antibiotics, Toxicities, and Emergency Antidotes",
        "total_questions": 6,
        "total_marks": 100,
        "duration_minutes": 45,
        "negative_marking": 0.33,
        "subjects": ["Clinical Pharmacology"],
        "year": "2024 High-Yield",
        "difficulty": "Moderate",
        "cutoff_reference": 60
    },
    {
        "id": "cms-psm-national-programs",
        "title": "National Health Programs & Epidemiology Vault",
        "subtitle": "NTEP (TB), UIP (Vaccines), NVBDCP, and Demography Indices",
        "total_questions": 6,
        "total_marks": 100,
        "duration_minutes": 45,
        "negative_marking": 0.33,
        "subjects": ["Preventive & Social Medicine"],
        "year": "2024 High-Yield",
        "difficulty": "Moderate",
        "cutoff_reference": 65
    },
    {
        "id": "esic-imo-clinical-drill",
        "title": "ESIC Insurance Medical Officer (IMO) High-Yield Drill",
        "subtitle": "Clinical Outpatient & Emergency Medicine Scenarios",
        "total_questions": 10,
        "total_marks": 100,
        "duration_minutes": 60,
        "negative_marking": 0.25,
        "subjects": ["Emergency Medicine", "Pharmacology", "General Medicine"],
        "year": "2023-2024 Cadre",
        "difficulty": "Standard Clinical",
        "cutoff_reference": 65
    }
]

EXAM_QUESTIONS: Dict[str, List[Dict[str, Any]]] = {
    "upsc-cms-paper-1": [
        {
            "id": "cms1-01",
            "subject": "General Medicine",
            "text": "A 58-year-old male with a history of long-standing hypertension presents with sudden onset retrosternal chest pain radiating to the interscapular region. Blood pressure is 186/110 mmHg in the right arm and 142/86 mmHg in the left arm. A grade II early diastolic decrescendo murmur is heard at the right sternal border. What is the most sensitive and initial diagnostic modality of choice in this hemodynamically stable patient?",
            "options": [
                "Transthoracic Echocardiogram (TTE)",
                "CT Angiography of the Chest with IV contrast",
                "Magnetic Resonance Angiography (MRA)",
                "Standard 12-lead ECG and Troponin I serial levels"
            ],
            "correct_option": 1,
            "explanation": "The clinical presentation (severe tearing chest pain radiating to back, asymmetric arm BP >20 mmHg, and new aortic regurgitation murmur) is classic for Acute Aortic Dissection (Stanford Type A). In a hemodynamically stable patient, CT Angiography of the chest is the most sensitive (98-100%) and preferred initial investigation of choice. In unstable patients, Transesophageal Echocardiography (TEE) or bedside TTE is preferred.",
            "citation": "Harrison's Principles of Internal Medicine, 21st Edition, Chapter 274: Diseases of the Aorta"
        },
        {
            "id": "cms1-02",
            "subject": "General Medicine",
            "text": "A 42-year-old female presents with persistent fatigue, cold intolerance, and constipation. Laboratory investigations reveal: TSH = 18.4 mIU/L (Normal: 0.4–4.0), Free T4 = 0.5 ng/dL (Normal: 0.8–1.8), and elevated anti-Thyroperoxidase (anti-TPO) antibodies. What is the standard starting dose of Levothyroxine for this patient with primary overt hypothyroidism?",
            "options": [
                "12.5 mcg daily",
                "25 mcg daily",
                "1.6 mcg/kg body weight daily",
                "100 mcg twice weekly"
            ],
            "correct_option": 2,
            "explanation": "In young to middle-aged patients without underlying coronary artery disease or cardiac arrhythmias, the full replacement dose of Levothyroxine is approximately 1.6 mcg/kg/day taken orally on an empty stomach 30-60 minutes before breakfast. In elderly patients or those with ischemic heart disease, treatment is started low (12.5–25 mcg/day) and titrated gradually.",
            "citation": "Harrison's Endocrinology, 4th Edition, Chapter on Hypothyroidism"
        },
        {
            "id": "cms1-03",
            "subject": "General Medicine",
            "text": "In a patient presenting with Diabetic Ketoacidosis (DKA) with Blood Glucose = 440 mg/dL, pH = 7.18, Serum Potassium = 3.1 mEq/L, and Urine Ketones +++, which of the following is the CORRECT immediate therapeutic priority?",
            "options": [
                "Start IV Regular Insulin bolus (0.1 units/kg) immediately",
                "Start aggressive IV 0.9% Normal Saline hydration and IV Potassium replacement BEFORE administering insulin",
                "Administer IV Sodium Bicarbonate infusion immediately",
                "Administer IV 5% Dextrose infusion"
            ],
            "correct_option": 1,
            "explanation": "CRITICAL EMERGENCY PROTOCOL: If serum potassium is < 3.3 mEq/L in DKA, insulin administration MUST BE WITHHELD while IV fluid resuscitation and potassium repletion (20-30 mEq/hr) are initiated. Giving insulin immediately would drive potassium into cells and precipitate life-threatening cardiac arrhythmias, respiratory muscle paralysis, or cardiac arrest.",
            "citation": "ADA Standards of Medical Care in Diabetes; Harrison's Principles of Internal Medicine"
        },
        {
            "id": "cms1-04",
            "subject": "General Medicine",
            "text": "A 35-year-old male from an endemic area presents with high fever with rigors occurring every alternate day, severe headache, and splenomegaly. Peripheral blood smear confirms Plasmodium vivax infection. Which drug is mandatory to prevent relapses by eradicating dormant hypnozoites in the liver, provided the patient is not G6PD deficient?",
            "options": [
                "Chloroquine for 3 days",
                "Primaquine 0.25 mg/kg daily for 14 days",
                "Artesunate plus Lumefantrine",
                "Doxycycline 100 mg twice daily for 7 days"
            ],
            "correct_option": 1,
            "explanation": "For radical cure of Plasmodium vivax and Plasmodium ovale malaria, Chloroquine or ACT clears the blood-stage schizonts, but Primaquine (0.25 mg/kg/day for 14 days) is essential to eradicate the persistent exoerythrocytic hypnozoites in the liver. G6PD status must be verified before prescribing Primaquine to avoid severe hemolytic anemia.",
            "citation": "NVBDCP National Drug Policy on Malaria; Harrison's Infectious Diseases"
        },
        {
            "id": "cms1-05",
            "subject": "Pediatrics",
            "text": "According to the National Immunization Schedule (NIS) of India, what is the correct age of administration for the first dose of the Measles-Rubella (MR) vaccine along with Vitamin A supplementation?",
            "options": [
                "At 6 weeks of age",
                "At 9 completed months to 12 months",
                "At 14 weeks of age",
                "At 16 to 24 months of age"
            ],
            "correct_option": 1,
            "explanation": "Under the Universal Immunization Programme (UIP) of India, MR 1st dose (0.5 mL subcutaneous in right upper arm) is administered upon completion of 9 months up to 12 months, accompanied by the 1st dose of Vitamin A (100,000 IU orally). The 2nd MR dose is given at 16-24 months with 200,000 IU Vitamin A.",
            "citation": "OP Ghai Essential Pediatrics, 9th Edition; MoHFW Universal Immunization Guidelines"
        },
        {
            "id": "cms1-06",
            "subject": "Pediatrics",
            "text": "A 2-year-old child presents with severe generalized bilateral pitting edema, moon face, sparse hypopigmented hair with 'flag sign', and apathy. Appetite is poor and weight-for-height Z-score is -2.5 SD. This presentation is most characteristic of which form of Severe Acute Malnutrition (SAM)?",
            "options": [
                "Marasmus",
                "Kwashiorkor (Edematous Malnutrition)",
                "Nutritional Rickets",
                "Congenital Nephrotic Syndrome"
            ],
            "correct_option": 1,
            "explanation": "Kwashiorkor is characterized by bilateral pedal/generalized pitting edema, preserved subcutaneous fat, hepatomegaly due to fatty infiltration, 'flag sign' (alternating bands of dark and light hair), and psychiatric changes (apathy and irritability). Marasmus, by contrast, presents with severe muscle wasting, absent subcutaneous fat, 'old man facies', and an alert, voracious appetite without edema.",
            "citation": "WHO Guidelines on Severe Acute Malnutrition; Ghai Essential Pediatrics"
        },
        {
            "id": "cms1-07",
            "subject": "General Medicine",
            "text": "Which of the following is the hallmark finding on bone marrow aspiration that confirms a diagnosis of Visceral Leishmaniasis (Kala-Azar)?",
            "options": [
                "Presence of amastigotes (Leishman-Donovan bodies) inside macrophages",
                "Flagellated promastigotes in extracellular fluid",
                "Reed-Sternberg giant cells",
                "Auer rods in myeloblasts"
            ],
            "correct_option": 0,
            "explanation": "Demonstration of Leishman-Donovan (LD) bodies—which are the intracellular, non-flagellated amastigote form of Leishmania donovani inside reticuloendothelial macrophages—in bone marrow or splenic aspirate smears confirms Kala-Azar. The flagellated promastigote form is found only in the gut of the sandfly vector (Phlebotomus argentipes) or in culture.",
            "citation": "Harrison's Principles of Internal Medicine; Park's Textbook of Preventive and Social Medicine"
        },
        {
            "id": "cms1-08",
            "subject": "General Medicine",
            "text": "A 65-year-old male with chronic COPD presents to casualty with acute exacerbation. Arterial Blood Gas (ABG) analysis shows: pH = 7.24, PaCO2 = 68 mmHg, PaO2 = 54 mmHg, HCO3 = 28 mEq/L. What is the primary acid-base disturbance?",
            "options": [
                "Metabolic Acidosis with respiratory compensation",
                "Acute on Chronic Respiratory Acidosis",
                "Uncompensated Respiratory Alkalosis",
                "Mixed Metabolic and Respiratory Alkalosis"
            ],
            "correct_option": 1,
            "explanation": "pH < 7.35 indicates acidosis. Elevated PaCO2 (>45 mmHg) confirms respiratory acidosis. The elevated bicarbonate (28 mEq/L) represents chronic renal compensation for longstanding CO2 retention, but the low pH indicates acute worsening (decompensation), making this an Acute on Chronic Respiratory Acidosis.",
            "citation": "Harrison's Principles of Internal Medicine, Chapter: Acidosis and Alkalosis"
        },
        {
            "id": "cms1-09",
            "subject": "Pediatrics",
            "text": "An 18-month-old child presents with a barking cough, inspiratory stridor, and hoarseness of voice that worsens at night. An anteroposterior soft tissue neck radiograph reveals the classic 'Steeple Sign' (subglottic narrowing). What is the primary etiology and drug of choice?",
            "options": [
                "Bacterial tracheitis; IV Vancomycin",
                "Croup (Laryngotracheobronchitis) caused by Parainfluenza virus; Oral Dexamethasone",
                "Acute Epiglottitis caused by Hib; IV Ceftriaxone",
                "Foreign body aspiration; Rigid bronchoscopy"
            ],
            "correct_option": 1,
            "explanation": "The clinical triad of barking 'seal-like' cough, inspiratory stridor, and hoarseness with the radiological 'Steeple sign' confirms Croup (Acute Laryngotracheobronchitis), most commonly caused by Human Parainfluenza virus type 1. Oral single-dose Dexamethasone (0.15–0.6 mg/kg) is the cornerstone treatment, supplemented with nebulized L-epinephrine in severe respiratory distress.",
            "citation": "Nelson Textbook of Pediatrics, 21st Edition; Ghai Essential Pediatrics"
        },
        {
            "id": "cms1-10",
            "subject": "General Medicine",
            "text": "Which drug is recognized as the first-line disease-modifying antirheumatic drug (DMARD) of choice for initial therapy in Rheumatoid Arthritis?",
            "options": [
                "Hydroxychloroquine",
                "Methotrexate",
                "Infliximab",
                "Sulfasalazine"
            ],
            "correct_option": 1,
            "explanation": "Methotrexate (starting at 7.5 to 15 mg once weekly orally along with Folic acid supplementation) is universally recognized by ACR and EULAR as the anchor first-line conventional synthetic DMARD for active rheumatoid arthritis.",
            "citation": "Harrison's Rheumatology; ACR Guidelines for Management of Rheumatoid Arthritis"
        },
        {
            "id": "cms1-11",
            "subject": "General Medicine",
            "text": "A 24-year-old medical intern sustains an accidental needle-stick injury while drawing blood from an HIV-positive patient with high viral load. Post-Exposure Prophylaxis (PEP) should ideally be initiated within how many hours of exposure?",
            "options": [
                "Within 2 hours (and not later than 72 hours)",
                "Within 7 days",
                "Within 14 days",
                "Only if antibody tests turn positive at 6 weeks"
            ],
            "correct_option": 0,
            "explanation": "According to NACO and WHO guidelines, Post-Exposure Prophylaxis (PEP) for HIV should be initiated as soon as possible, ideally within 2 hours, and no later than 72 hours post-exposure. Standard PEP regimen consists of a 28-day course of triple antiretroviral therapy (e.g. Tenofovir + Lamivudine + Dolutegravir).",
            "citation": "NACO National Guidelines for Post-Exposure Prophylaxis, MoHFW"
        },
        {
            "id": "cms1-12",
            "subject": "Pediatrics",
            "text": "A neonate is evaluated at 1 minute and 5 minutes after birth. At 5 minutes: Heart rate = 110 bpm, Respiration = strong cry, Muscle tone = active motion and well-flexed extremities, Reflex irritability = vigorous cry on stimulation, Color = body pink with blue extremities (acrocyanosis). What is the Apgar score?",
            "options": [
                "10",
                "9",
                "8",
                "7"
            ],
            "correct_option": 1,
            "explanation": "Apgar components: Heart rate > 100 bpm = 2; Respiration (strong cry) = 2; Muscle tone (active motion) = 2; Reflex irritability (vigorous cry) = 2; Color (acrocyanosis / pink body with blue hands/feet) = 1. Total score = 2 + 2 + 2 + 2 + 1 = 9.",
            "citation": "Nelson Textbook of Pediatrics; Ghai Essential Pediatrics"
        }
    ],

    "upsc-cms-paper-2": [
        {
            "id": "cms2-01",
            "subject": "General Surgery",
            "text": "A 28-year-old male presents with periumbilical colicky abdominal pain that shifts to the right lower quadrant after 8 hours. On examination, localized tenderness, guarding, and rebound tenderness are noted at McBurney's point. Rovsing's sign and Psoas sign are positive. What is the most appropriate management?",
            "options": [
                "Empiric oral antibiotics and observation for 48 hours",
                "Immediate Appendectomy (Laparoscopic or Open)",
                "Barium Enema examination",
                "Colonoscopy with mucosal biopsy"
            ],
            "correct_option": 1,
            "explanation": "The shifting of pain (visceral to somatic) with signs of localized peritoneal inflammation at McBurney's point is hallmark for Acute Appendicitis. Early surgical intervention (Appendectomy) remains the definitive gold standard to prevent perforation, gangrene, and peritonitis.",
            "citation": "Bailey & Love's Short Practice of Surgery, 28th Edition, Chapter on The Vermiform Appendix"
        },
        {
            "id": "cms2-02",
            "subject": "General Surgery",
            "text": "Which anatomical structure forms the inferior boundary of the Calot's Triangle (Hepatocystic Triangle), an essential landmark in Laparoscopic Cholecystectomy?",
            "options": [
                "Common Hepatic Duct",
                "Cystic Duct",
                "Inferior border of liver",
                "Cystic Artery"
            ],
            "correct_option": 1,
            "explanation": "Anatomy of Calot's (Hepatocystic) triangle: Medial border = Common Hepatic Duct; Inferior/Lateral border = Cystic Duct; Superior border = Inferior surface of liver segment V. The triangle contains the Cystic Artery and Lund's lymph node.",
            "citation": "Bailey & Love's Short Practice of Surgery; Fischer's Mastery of Surgery"
        },
        {
            "id": "cms2-03",
            "subject": "Obstetrics & Gynaecology",
            "text": "A 32-week pregnant primigravida presents with headache, scotoma, and blood pressure of 166/112 mmHg recorded on two occasions 4 hours apart. Urine dipstick shows +++ proteinuria. What is the anticonvulsant drug of choice to prevent and treat eclamptic seizures?",
            "options": [
                "IV Diazepam",
                "IV Phenytoin",
                "Magnesium Sulphate (Pritchard or Zuspan regimen)",
                "Oral Levetiracetam"
            ],
            "correct_option": 2,
            "explanation": "Magnesium Sulphate is the proven drug of choice worldwide (confirmed by the landmark Collaborative Eclampsia Trial) for prevention and control of seizures in severe pre-eclampsia and eclampsia. Pritchard regimen involves 4g IV + 10g IM loading dose, followed by 5g IM maintenance dose every 4 hours.",
            "citation": "DC Dutta's Textbook of Obstetrics, 9th Edition; Williams Obstetrics"
        },
        {
            "id": "cms2-04",
            "subject": "Obstetrics & Gynaecology",
            "text": "What is the defining criterion for Postpartum Hemorrhage (PPH) following a normal vaginal delivery according to WHO guidelines?",
            "options": [
                "Blood loss exceeding 200 mL within 24 hours",
                "Blood loss exceeding 500 mL within 24 hours",
                "Blood loss exceeding 1000 mL within 24 hours",
                "Any blood loss that causes a hemoglobin drop of 1 g/dL"
            ],
            "correct_option": 1,
            "explanation": "According to WHO, Postpartum Hemorrhage (PPH) is defined as blood loss of 500 mL or more within 24 hours after vaginal birth, or 1000 mL or more after cesarean section. Uterine atony is responsible for ~80% of primary PPH cases.",
            "citation": "WHO Recommendations for the Prevention and Treatment of Postpartum Haemorrhage; DC Dutta's Obstetrics"
        },
        {
            "id": "cms2-05",
            "subject": "Preventive & Social Medicine",
            "text": "In epidemiological screening, the ability of a diagnostic test to correctly identify all those who truly have the disease is defined as:",
            "options": [
                "Specificity",
                "Sensitivity",
                "Positive Predictive Value",
                "Negative Predictive Value"
            ],
            "correct_option": 1,
            "explanation": "Sensitivity is the true positive rate: the probability that a test is positive given that the patient has the disease [TP / (TP + FN)]. Specificity is the true negative rate: the probability that a test is negative in a disease-free individual [TN / (TN + FP)].",
            "citation": "Park's Textbook of Preventive and Social Medicine, 26th Edition, Chapter on Screening for Disease"
        },
        {
            "id": "cms2-06",
            "subject": "Preventive & Social Medicine",
            "text": "What is the primary vector responsible for the transmission of Dengue and Chikungunya viruses in urban Indian environments?",
            "options": [
                "Anopheles stephensi",
                "Culex quinquefasciatus",
                "Aedes aegypti",
                "Mansonia annulifera"
            ],
            "correct_option": 2,
            "explanation": "Aedes aegypti (tiger mosquito) is the primary daytime-biting domestic vector for Dengue, Chikungunya, and Zika. It breeds in clean, artificial collections of stagnant water (air coolers, discarded tyres, overhead cisterns).",
            "citation": "Park's Textbook of Preventive and Social Medicine; NVBDCP Guidelines"
        },
        {
            "id": "cms2-07",
            "subject": "General Surgery",
            "text": "According to the Parkland Formula, what is the total crystalloid fluid requirement in the first 24 hours for a 70 kg adult patient suffering from 40% second-degree thermal burns?",
            "options": [
                "5,600 mL",
                "11,200 mL (with half given in first 8 hours)",
                "8,400 mL",
                "14,000 mL"
            ],
            "correct_option": 1,
            "explanation": "Parkland Formula: Total Fluid (Ringer's Lactate) = 4 mL × Body weight in kg × % TBSA burn = 4 × 70 × 40 = 11,200 mL. Half (5,600 mL) must be infused in the first 8 hours from the TIME OF INJURY, and the remaining half over the subsequent 16 hours.",
            "citation": "Bailey & Love's Short Practice of Surgery, Chapter on Burns; ATLS Manual"
        },
        {
            "id": "cms2-08",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which of the following is the most common cause of early recurrent spontaneous pregnancy loss (recurrent miscarriage) in the first trimester?",
            "options": [
                "Fetal chromosomal abnormalities (Aneuploidy)",
                "Cervical incompetence",
                "Uncontrolled gestational diabetes",
                "Bicornuate uterus"
            ],
            "correct_option": 0,
            "explanation": "Chromosomal anomalies (aneuploidies like autosomal trisomies, monosomy X, and triploidy) account for 50-70% of all spontaneous first-trimester miscarriages. Anatomical factors like cervical incompetence typically cause painless mid-trimester (second trimester) losses.",
            "citation": "Williams Obstetrics, 26th Edition; DC Dutta's Gynaecology"
        },
        {
            "id": "cms2-09",
            "subject": "Preventive & Social Medicine",
            "text": "Under the Indian Public Health Standards (IPHS), a Primary Health Centre (PHC) is established to cater to what population size in plain areas versus hilly/tribal areas?",
            "options": [
                "5,000 (Plain) and 3,000 (Hilly/Tribal)",
                "30,000 (Plain) and 20,000 (Hilly/Tribal)",
                "1,20,000 (Plain) and 80,000 (Hilly/Tribal)",
                "10,000 (Plain) and 5,000 (Hilly/Tribal)"
            ],
            "correct_option": 1,
            "explanation": "IPHS Population Norms: Sub-Centre = 5,000 (Plain) / 3,000 (Hilly/Tribal); Primary Health Centre (PHC) = 30,000 (Plain) / 20,000 (Hilly/Tribal); Community Health Centre (CHC) = 1,20,000 (Plain) / 80,000 (Hilly/Tribal).",
            "citation": "Park's Textbook of Preventive and Social Medicine; IPHS Guidelines MoHFW"
        },
        {
            "id": "cms2-10",
            "subject": "General Surgery",
            "text": "A 45-year-old male with a history of peptic ulcer disease presents with sudden excruciating upper abdominal pain. On physical exam, the abdomen is rigid and 'board-like'. Upright chest X-ray confirms free air (crescent of gas) under the right dome of the diaphragm. What is the diagnosis?",
            "options": [
                "Acute Pancreatitis",
                "Perforated Peptic Ulcer",
                "Strangulated Inguinal Hernia",
                "Acute Mesenteric Ischemia"
            ],
            "correct_option": 1,
            "explanation": "Sudden onset severe generalized abdominal pain with board-like muscular rigidity and pneumoperitoneum (free gas under the diaphragm) is pathognomonic for hollow viscus perforation, most commonly a perforated anterior duodenal or gastric ulcer requiring emergency exploratory laparotomy and Graham's omental patch repair.",
            "citation": "Bailey & Love's Short Practice of Surgery, Chapter on Stomach and Duodenum"
        },
        {
            "id": "cms2-11",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which hormone is responsible for triggering the mid-cycle LH surge that leads directly to ovulation in a normal menstrual cycle?",
            "options": [
                "Progesterone",
                "Sustained peak of 17-beta Estradiol",
                "Inhibin B",
                "Human Chorionic Gonadotropin"
            ],
            "correct_option": 1,
            "explanation": "A critical threshold of Estradiol (>200 pg/mL sustained for at least 48 to 50 hours) secreted by the dominant graafian follicle exerts positive feedback on the pituitary gland and hypothalamus, triggering the massive Luteinizing Hormone (LH) surge that induces ovulation ~34 to 36 hours later.",
            "citation": "DC Dutta's Textbook of Gynaecology; Speroff's Clinical Gynecologic Endocrinology"
        },
        {
            "id": "cms2-12",
            "subject": "Preventive & Social Medicine",
            "text": "Which of the following is considered the single most sensitive indicator of overall community health and socioeconomic development in a country?",
            "options": [
                "Maternal Mortality Ratio (MMR)",
                "Infant Mortality Rate (IMR)",
                "Crude Death Rate (CDR)",
                "Annual Parasite Index (API)"
            ],
            "correct_option": 1,
            "explanation": "Infant Mortality Rate (IMR)—number of infant deaths under 1 year of age per 1,000 live births in a given year—is universally regarded as the most sensitive single index of health, sanitation, nutrition, and general socioeconomic conditions of a population.",
            "citation": "Park's Textbook of Preventive and Social Medicine, Chapter on Demography and Family Planning"
        }
    ],

    "cms-clinical-pharma": [
        {
            "id": "pharma-01",
            "subject": "Clinical Pharmacology",
            "text": "Which of the following is the specific antidote for acute Paracetamol (Acetaminophen) toxicity and what is its primary mechanism of action?",
            "options": [
                "N-Acetylcysteine (NAC); replenishes intracellular glutathione reserves",
                "Flumazenil; competitive antagonism at GABA-A receptors",
                "Deferoxamine; chelates free iron ions",
                "Pralidoxime; reactivates acetylcholinesterase enzyme"
            ],
            "correct_option": 0,
            "explanation": "N-Acetylcysteine (NAC) acts as a glutathione precursor and substitute, binding and detoxifying the hepatotoxic reactive metabolite N-acetyl-p-benzoquinone imine (NAPQI). It is most effective when administered within 8-10 hours of paracetamol ingestion.",
            "citation": "KD Tripathi's Essentials of Medical Pharmacology, 8th Edition; Harrison's Toxicology"
        },
        {
            "id": "pharma-02",
            "subject": "Clinical Pharmacology",
            "text": "A 30-year-old pregnant patient in her third trimester presents with acute pyelonephritis. Which of the following antimicrobial classes is strictly CONTRAINDICATED due to the risk of fetal arthropathy and cartilage damage?",
            "options": [
                "Cephalosporins (e.g. Ceftriaxone)",
                "Fluoroquinolones (e.g. Ciprofloxacin)",
                "Penicillins (e.g. Amoxicillin-Clavulanate)",
                "Macrolides (e.g. Azithromycin)"
            ],
            "correct_option": 1,
            "explanation": "Fluoroquinolones (Ciprofloxacin, Levofloxacin) are contraindicated in pregnancy because they bind to developing connective tissue and cartilage, causing fetal arthropathy and chondrodysplasia in animal studies. Cephalosporins and aminopenicillins are safe in pregnancy.",
            "citation": "KD Tripathi's Essentials of Medical Pharmacology; Briggs Drugs in Pregnancy and Lactation"
        },
        {
            "id": "pharma-03",
            "subject": "Clinical Pharmacology",
            "text": "Which oral anticoagulant acts as a direct Factor Xa inhibitor and does NOT require routine monitoring of PT/INR?",
            "options": [
                "Warfarin",
                "Rivaroxaban",
                "Dabigatran",
                "Unfractionated Heparin"
            ],
            "correct_option": 1,
            "explanation": "Rivaroxaban and Apixaban are Direct Oral Anticoagulants (DOACs) that selectively inhibit Factor Xa directly. Dabigatran, by contrast, is a direct thrombin (Factor IIa) inhibitor. Warfarin requires strict PT/INR monitoring.",
            "citation": "Harrison's Principles of Internal Medicine; KD Tripathi's Pharmacology"
        },
        {
            "id": "pharma-04",
            "subject": "Clinical Pharmacology",
            "text": "Which drug is the treatment of choice for acute anaphylactic shock and what is the recommended adult dose and route?",
            "options": [
                "Epinephrine (Adrenaline) 1:1,000, 0.5 mg Intramuscular in the anterolateral thigh",
                "Epinephrine (Adrenaline) 1:10,000, 1.0 mg rapid IV bolus",
                "Hydrocortisone 100 mg IV alone",
                "Diphenhydramine 50 mg oral"
            ],
            "correct_option": 0,
            "explanation": "Intramuscular Epinephrine (1:1,000 dilution, 0.5 mg in adults, 0.01 mg/kg in children) injected into the vastus lateralis (anterolateral thigh) is the immediate first-line lifesaving drug in anaphylaxis. IV epinephrine bolus without dilution poses severe risk of ventricular fibrillation and cerebral hemorrhage.",
            "citation": "Resuscitation Council UK Anaphylaxis Guidelines; Harrison's Allergy and Clinical Immunology"
        },
        {
            "id": "pharma-05",
            "subject": "Clinical Pharmacology",
            "text": "The classic 'Red Man Syndrome' characterized by flushing, erythema, and pruritus of the face and upper torso is an infusion-related adverse reaction caused by which antibiotic?",
            "options": [
                "Vancomycin",
                "Gentamicin",
                "Clindamycin",
                "Amphotericin B"
            ],
            "correct_option": 0,
            "explanation": "Red Man Syndrome is an adverse reaction caused by rapid intravenous infusion of Vancomycin leading to direct, non-IgE-mediated histamine release from mast cells. It is prevented by slow infusion over at least 60 minutes and pre-treatment with antihistamines.",
            "citation": "KD Tripathi's Essentials of Medical Pharmacology; Goodman & Gilman's Pharmacological Basis of Therapeutics"
        },
        {
            "id": "pharma-06",
            "subject": "Clinical Pharmacology",
            "text": "A patient on chronic Lithium therapy for Bipolar Disorder is started on Hydrochlorothiazide for hypertension. What dangerous drug interaction is likely to occur?",
            "options": [
                "Severe Lithium Toxicity due to decreased renal clearance",
                "Rapid loss of Lithium efficacy due to enhanced excretion",
                "Severe Hyperkalemia",
                "Acute pancreatitis"
            ],
            "correct_option": 0,
            "explanation": "Thiazide diuretics cause sodium depletion at the distal convoluted tubule, which triggers compensatory increased reabsorption of sodium AND lithium in the proximal tubule. This reduces lithium clearance by 25-40% and precipitates severe lithium toxicity (tremors, ataxia, seizures, arrhythmias).",
            "citation": "Harrison's Principles of Internal Medicine; KD Tripathi's Pharmacology"
        }
    ],

    "cms-psm-national-programs": [
        {
            "id": "psm-01",
            "subject": "Preventive & Social Medicine",
            "text": "Under the National Tuberculosis Elimination Program (NTEP) of India, what is the standard first-line intensive phase regimen for drug-sensitive pulmonary tuberculosis in adults?",
            "options": [
                "2 months of daily HRZE (Isoniazid, Rifampicin, Pyrazinamide, Ethambutol)",
                "2 months of thrice-weekly HRZ",
                "6 months of daily Rifampicin alone",
                "3 months of Bedaquiline + Delamanid"
            ],
            "correct_option": 0,
            "explanation": "Under NTEP, the standard treatment regimen for drug-sensitive TB consists of an Intensive Phase of 2 months of daily fixed-dose combinations of 4 drugs: HRZE (Isoniazid, Rifampicin, Pyrazinamide, Ethambutol), followed by a Continuation Phase of 4 months of 3 drugs: HRE (Isoniazid, Rifampicin, Ethambutol).",
            "citation": "NTEP Guidelines, Central TB Division, MoHFW; Park's PSM 26th Edition"
        },
        {
            "id": "psm-02",
            "subject": "Preventive & Social Medicine",
            "text": "Under the Universal Immunization Programme (UIP) of India, which vaccine is administered intradermally at birth or up to 1 year of age over the left deltoid?",
            "options": [
                "BCG (Bacillus Calmette-Guérin)",
                "Hepatitis B birth dose",
                "Oral Polio Vaccine (OPV-0)",
                "Inactivated Polio Vaccine (fIPV)"
            ],
            "correct_option": 0,
            "explanation": "BCG is given intradermally (0.05 mL at birth or 0.1 mL after 1 month up to 1 year) over the left deltoid insertion. A permanent wheal appears, followed in 2-3 weeks by a papule that crusts and forms a typical permanent round scar by 6-12 weeks.",
            "citation": "Universal Immunization Programme Guidelines, MoHFW; Park's PSM"
        },
        {
            "id": "psm-03",
            "subject": "Preventive & Social Medicine",
            "text": "What is the key epidemiological criterion defined by the NVBDCP to confirm that a malaria-endemic area has entered the pre-elimination/elimination phase?",
            "options": [
                "Annual Parasite Index (API) < 1 case per 1,000 population at risk",
                "Slide Positivity Rate (SPR) > 5%",
                "Infant Parasite Rate (IPR) > 10%",
                "Annual Blood Examination Rate (ABER) < 2%"
            ],
            "correct_option": 0,
            "explanation": "The Annual Parasite Index (API = confirmed malaria cases in a year / total population × 1,000) is the primary index to assess malaria transmission. An API < 1 case per 1,000 population indicates that the district has entered the malaria pre-elimination phase.",
            "citation": "NVBDCP National Strategic Plan for Malaria Elimination in India; Park's PSM"
        },
        {
            "id": "psm-04",
            "subject": "Preventive & Social Medicine",
            "text": "According to the Janani Suraksha Yojana (JSY) guidelines, what is the primary objective of the program and how is it implemented?",
            "options": [
                "Promote institutional deliveries among pregnant women via cash incentives to reduce Maternal and Neonatal Mortality",
                "Provide free school meals to adolescent girls",
                "Eradicate iron deficiency in preschool children",
                "Offer compulsory tubectomy incentives"
            ],
            "correct_option": 0,
            "explanation": "Janani Suraksha Yojana (JSY) is a safe motherhood intervention under NHM that integrates cash assistance with antenatal care and institutional delivery in government or accredited private health facilities, directly targeting reductions in MMR and NMR.",
            "citation": "National Health Mission Guidelines; Park's Textbook of Preventive and Social Medicine"
        },
        {
            "id": "psm-05",
            "subject": "Preventive & Social Medicine",
            "text": "Under the Biomedical Waste Management Rules (2016) in India, into which color-coded container must contaminated anatomical waste (placenta, amputated limbs) and soiled bandages be discarded?",
            "options": [
                "Yellow non-chlorinated plastic bag (for Incineration / Deep burial)",
                "Red container (for Autoclaving and recycling)",
                "Blue cardboard box (for Glassware and ampoules)",
                "Translucent white puncture-proof container (for Needles and sharps)"
            ],
            "correct_option": 0,
            "explanation": "BMWM Rules 2016: Yellow bags = Human anatomical waste, animal waste, soiled dressings, expired cytotoxic medicines (treated via incineration or plasma pyrolysis). Red = Contaminated recyclable plastics (catheters, IV tubing). White translucent = Needles, scalpels, sharps. Blue = Glassware and metallic body implants.",
            "citation": "Biomedical Waste Management Rules 2016, Ministry of Environment, Forest and Climate Change; Park's PSM"
        },
        {
            "id": "psm-06",
            "subject": "Preventive & Social Medicine",
            "text": "What is the targeted replacement-level Total Fertility Rate (TFR) required for a population to achieve stabilization?",
            "options": [
                "2.1 children per woman",
                "1.5 children per woman",
                "2.8 children per woman",
                "3.0 children per woman"
            ],
            "correct_option": 0,
            "explanation": "Replacement-level fertility is the average number of children that a couple must bear in their reproductive lifetime to replace themselves. In demography, a Total Fertility Rate (TFR) of 2.1 is defined as replacement level fertility.",
            "citation": "NFHS-5 Report; Park's Textbook of Preventive and Social Medicine, Demography chapter"
        }
    ],

    "esic-imo-clinical-drill": [
        {
            "id": "esic-01",
            "subject": "Emergency Medicine",
            "text": "An agricultural industrial worker is brought to casualty with excessive salivation, pinpoint pupils (miosis), bilateral diffuse rhonchi, bradycardia, and fasciculations following pesticide exposure. What is the immediate pharmacological antidote of choice?",
            "options": [
                "Atropine Sulfate IV until signs of full atropinization (clearing of bronchorrhea) appear",
                "Physostigmine IV",
                "Naloxone IV",
                "Sodium Thiosulfate IV"
            ],
            "correct_option": 0,
            "explanation": "The clinical picture of SLUDGE (Salivation, Lacrimation, Urination, Defecation, GI cramps, Emesis) with miosis and bronchorrhea confirms acute Organophosphate Poisoning. Intravenous Atropine (1.8-3 mg bolus, doubled every 5 minutes until pulmonary secretions clear and heart rate >80 bpm) is the immediate lifesaving muscarinic antagonist.",
            "citation": "Harrison's Principles of Internal Medicine; KD Tripathi's Medical Pharmacology"
        },
        {
            "id": "esic-02",
            "subject": "General Medicine",
            "text": "A 52-year-old factory supervisor presents to the dispensary with crushing retrosternal chest pain of 45 minutes duration. 12-lead ECG reveals 3 mm ST-segment elevation in leads V1 to V4. What is the immediate antiplatelet loading dose protocol recommended prior to emergency referral for PCI or thrombolysis?",
            "options": [
                "Aspirin 325 mg chewed + Clopidogrel 300-600 mg oral load",
                "Low molecular weight heparin alone",
                "Aspirin 75 mg daily starting next morning",
                "Streptokinase 1.5 million units oral"
            ],
            "correct_option": 0,
            "explanation": "In acute ST-Elevation Myocardial Infarction (STEMI), Dual Antiplatelet Therapy (DAPT) with chewed non-enteric coated Aspirin (162-325 mg) plus a P2Y12 inhibitor (Clopidogrel 300-600 mg or Ticagrelor 180 mg) should be administered immediately upon diagnosis unless contraindicated.",
            "citation": "AHA/ACC STEMI Management Guidelines; Harrison's Cardiology"
        },
        {
            "id": "esic-03",
            "subject": "Preventive & Social Medicine",
            "text": "A patient presents with a deep transdermal dog bite on the right calf with active oozing of blood (WHO Category III exposure). What is the mandatory immediate post-exposure prophylaxis protocol?",
            "options": [
                "Immediate wound washing under running tap water with soap for 15 minutes, local infiltration of Rabies Immunoglobulin (RIG), and Modern Cell Culture Vaccine (IM on Days 0, 3, 7, 28)",
                "Anti-rabies vaccine alone on Day 0 and Day 3",
                "Primary suturing of the wound immediately under local anesthesia",
                "Tetanus toxoid only with observation of dog for 10 days"
            ],
            "correct_option": 0,
            "explanation": "WHO Category III animal bites (transdermal bites or scratches, licks on broken skin) strictly require: 1) Vigorous washing with soap and water for at least 15 minutes; 2) Rabies Immunoglobulin (HRIG 20 IU/kg) infiltrated directly into and around the wound; 3) Rabies vaccination on days 0, 3, 7, and 28. Wounds should NOT be primarily sutured.",
            "citation": "National Guidelines on Rabies Prophylaxis, NVBDCP / MoHFW; Park's PSM"
        },
        {
            "id": "esic-04",
            "subject": "Emergency Medicine",
            "text": "A 30-year-old patient is brought to casualty in continuous generalized tonic-clonic status epilepticus lasting >10 minutes. What is the first-line intravenous benzodiazepine of choice?",
            "options": [
                "IV Lorazepam (0.1 mg/kg given at 2 mg/min)",
                "IV Phenytoin 15 mg/kg bolus",
                "Oral Carbamazepine",
                "IV Propofol infusion"
            ],
            "correct_option": 0,
            "explanation": "Intravenous Lorazepam (0.1 mg/kg up to 4 mg bolus) is the universally preferred first-line agent for terminating early status epilepticus due to its rapid onset and longer duration of action in brain tissue compared to Diazepam.",
            "citation": "Neurocritical Care Society Guidelines for Status Epilepticus; Harrison's Neurology"
        },
        {
            "id": "esic-05",
            "subject": "General Medicine",
            "text": "Which chest X-ray finding is characteristically associated with Silicosis in stone-crushing and pottery industrial workers under the ESI Act?",
            "options": [
                "'Eggshell calcification' of hilar lymph nodes and multiple nodular opacities in upper lung zones",
                "Pleural plaques in lower lung zones with asbestosis",
                "Cavitation in bilateral apices with air-fluid levels",
                "Honeycombing with basal subpleural reticulation"
            ],
            "correct_option": 0,
            "explanation": "Eggshell calcification (peripheral rim calcification of enlarged hilar and mediastinal lymph nodes) along with diffuse rounded nodular opacities predominantly affecting the upper lung zones is pathognomonic for chronic Silicosis.",
            "citation": "Park's Textbook of Preventive and Social Medicine, Chapter on Occupational Health; Harrison's Pulmonology"
        },
        {
            "id": "esic-06",
            "subject": "Emergency Medicine",
            "text": "A rural laborer presents 2 hours after a Russel's Viper bite with severe local swelling, bleeding from gums, and prolonged Whole Blood Clotting Time (20WBCT > 20 minutes). How many vials of Polyvalent Anti-Snake Venom (ASV) are initially indicated?",
            "options": [
                "10 vials of reconstituted Polyvalent ASV infused in 0.9% Normal Saline over 1 hour",
                "1 vial administered subcutaneously",
                "2 vials administered intramuscularly",
                "50 vials given as rapid IV push"
            ],
            "correct_option": 0,
            "explanation": "According to the National Snakebite Management Protocol of India, in patients with systemic envenomation (hemotoxicity or neurotoxicity), the initial dose is 10 vials of Lyophilized Polyvalent Anti-Snake Venom (ASV) reconstituted in 500 mL of normal saline and infused intravenously over 1 hour.",
            "citation": "National Protocol for Management of Snakebites, MoHFW India"
        }
    ]
}
