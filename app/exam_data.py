import json
from typing import List, Dict, Any

EXAMS_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "upsc-cms-paper-1",
        "title": "UPSC Combined Medical Services (CMS) — Paper 1",
        "subtitle": "General Medicine (96 Qs) & Pediatrics (24 Qs)",
        "total_questions": 12, # representative high-yield set for immediate test run
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
    ]
}
