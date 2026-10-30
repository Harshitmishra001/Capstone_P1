import uuid
import datetime
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI(
    title="Silent Witness API",
    description="Backend ML API for analyzing eyewitness testimonies",
    version="1.0.0"
)

# Enable CORS for the Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-Memory Database (seeded from theft_case_output.json) ---
DB = {
    "incidents": [
        {
            "id": "inc-demo01",
            "title": "Tanishq Jewelry Heist — MG Road",
            "type": "Armed Robbery",
            "date": "2024-11-03",
            "status": "Reviewing",
            "witnessCount": 5,
            "contradictionCount": 17
        },
        {
            "id": "inc-demo02",
            "title": "Gold Vault Break-In — Commercial Street",
            "type": "Burglary",
            "date": "2024-11-10",
            "status": "Active",
            "witnessCount": 5,
            "contradictionCount": 17
        },
        {
            "id": "inc-demo03",
            "title": "ATM Cash Heist — Indiranagar",
            "type": "Theft",
            "date": "2024-10-22",
            "status": "Active",
            "witnessCount": 5,
            "contradictionCount": 17
        },
        {
            "id": "inc-demo04",
            "title": "Diamond Merchant Robbery — Chickpet",
            "type": "Armed Robbery",
            "date": "2024-09-14",
            "status": "Archived",
            "witnessCount": 5,
            "contradictionCount": 17
        },
        {
            "id": "inc-demo05",
            "title": "Bank Locker Fraud — Koramangala",
            "type": "Financial Fraud",
            "date": "2024-08-30",
            "status": "Active",
            "witnessCount": 5,
            "contradictionCount": 17
        }
    ],
    "incident_data": {
        "inc-demo01": {
            "statements": [
                {
                    "id": "stmt_0",
                    "witness": "Witness A",
                    "text": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_1",
                    "witness": "Witness B",
                    "text": "I run a café just across from the Tanishq store. I saw three robbers sprinted out of the store entrance carrying heavy duffel bags. Then the robbers pushed past frightened pedestrians on the sidewalk as people screamed for police assistance.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_2",
                    "witness": "Witness C",
                    "text": "On MG Road when the commotion erupted. The primary robber wore a dark leather jacket. The primary robber fled and then revved a motorcycle. The primary robber headed north toward the flyover.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_3",
                    "witness": "Witness D",
                    "text": "I was walking along MG Road. Suddenly the thieves dashed from the store. The primary robber was wearing a bright red hoodie with beige cargo pants.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_4",
                    "witness": "Witness E",
                    "text": "I was inside securing the cash register when I heard the alarm. The thieves took fifty lakhs worth of diamond necklaces and luxury watches from the vault counters. Emergency sirens began blaring within minutes.",
                    "status": "Processed"
                }
            ],
            "markers": [
                {
                    "id": "m_1",
                    "lat": 12.975,
                    "lng": 77.6069,
                    "label": "MG Road",
                    "witness": "Witness A",
                    "color": "blue"
                }
            ],
            "timeline": [
                {
                    "id": "ev_0",
                    "content": "I was stationed by the glass doors of the Tanishq showroom on MG Road",
                    "start": "2024-11-03T14:00:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_1",
                    "content": "Two masked robbers stormed inside",
                    "start": "2024-11-03T14:01:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_2",
                    "content": "The robbers ordered all customers to lie flat on the floor",
                    "start": "2024-11-03T14:02:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_3",
                    "content": "The primary robber was wearing a dark leather jacket and blue jeans",
                    "start": "2024-11-03T14:03:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_4",
                    "content": "I run",
                    "start": "2024-11-03T14:04:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_5",
                    "content": "three robbers sprinted out of the store entrance carrying heavy duffel bags",
                    "start": "2024-11-03T14:05:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_6",
                    "content": "the robbers pushed past frightened pedestrians on the sidewalk as people screamed for p...",
                    "start": "2024-11-03T14:06:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_7",
                    "content": "the commotion erupted",
                    "start": "2024-11-03T14:07:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_8",
                    "content": "the primary robber wore a dark leather jacket",
                    "start": "2024-11-03T14:08:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_9",
                    "content": "the primary robber fled",
                    "start": "2024-11-03T14:09:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_10",
                    "content": "the primary robber revved a motorcycle",
                    "start": "2024-11-03T14:10:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_11",
                    "content": "the primary robber headed",
                    "start": "2024-11-03T14:11:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_12",
                    "content": "I was walking along MG Road",
                    "start": "2024-11-03T14:12:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_13",
                    "content": "the thieves dashed",
                    "start": "2024-11-03T14:13:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_14",
                    "content": "The primary robber was wearing a bright red hoodie with beige cargo pants",
                    "start": "2024-11-03T14:14:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_15",
                    "content": "I securing the cash register",
                    "start": "2024-11-03T14:15:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_16",
                    "content": "The thieves took fifty lakhs worth of diamond necklaces and luxury watches from the vau...",
                    "start": "2024-11-03T14:16:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_17",
                    "content": "I emergency sirens began blaring",
                    "start": "2024-11-03T14:17:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                }
            ],
            "contradictions": [
                {
                    "id": "c_0",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #1",
                    "rationale": "The first statement specifies being stationed by glass doors of a Tanishq showroom, while the second only mentions walking along MG Road without mentioning any specific location or activity.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": " doors of the",
                            "fullText": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                            "span": [
                                28,
                                41
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "was walking",
                            "fullText": "I was walking along MG Road. Suddenly the thieves dashed from the store. The primary robber was wearing a bright red hoodie with beige cargo pants.",
                            "span": [
                                2,
                                13
                            ]
                        }
                    ]
                },
                {
                    "id": "c_1",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #2",
                    "rationale": "Statement 1 describes two masked robbers entering a location while Statement 2 mentions three robbers sprinting out carrying duffel bags.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "s ordered all ",
                            "fullText": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                            "span": [
                                116,
                                130
                            ]
                        },
                        {
                            "witness": "Witness B",
                            "snippet": "y duffel",
                            "fullText": "I run a café just across from the Tanishq store. I saw three robbers sprinted out of the store entrance carrying heavy duffel bags. Then the robbers pushed past frightened pedestrians on the sidewalk as people screamed for police assistance.",
                            "span": [
                                117,
                                125
                            ]
                        }
                    ]
                },
                {
                    "id": "c_2",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #3",
                    "rationale": "In Statement 1, it is stated that two masked robbers stormed inside; in contrast, Statement 2 mentions only one robber fleeing.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "s ordered all ",
                            "fullText": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                            "span": [
                                116,
                                130
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "mary",
                            "fullText": "On MG Road when the commotion erupted. The primary robber wore a dark leather jacket. The primary robber fled and then revved a motorcycle. The primary robber headed north toward the flyover.",
                            "span": [
                                147,
                                151
                            ]
                        }
                    ]
                },
                {
                    "id": "c_3",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #4",
                    "rationale": "The first statement mentions two masked robbers storming in while the second specifies that the primary robber was revving a motorcycle.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "s ordered all ",
                            "fullText": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                            "span": [
                                116,
                                130
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "oad ",
                            "fullText": "On MG Road when the commotion erupted. The primary robber wore a dark leather jacket. The primary robber fled and then revved a motorcycle. The primary robber headed north toward the flyover.",
                            "span": [
                                7,
                                11
                            ]
                        }
                    ]
                },
                {
                    "id": "c_4",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #5",
                    "rationale": "The primary robber in Statement 1 was described as wearing a dark leather jacket and blue jeans, while Statement 2 mentions three robbers sprinting out of the store entrance carrying heavy duffel bags without specifying attire.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "tatione",
                            "fullText": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness B",
                            "snippet": "y duffel",
                            "fullText": "I run a café just across from the Tanishq store. I saw three robbers sprinted out of the store entrance carrying heavy duffel bags. Then the robbers pushed past frightened pedestrians on the sidewalk as people screamed for police assistance.",
                            "span": [
                                117,
                                125
                            ]
                        }
                    ]
                },
                {
                    "id": "c_5",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #6",
                    "rationale": "The first statement specifies the attire of the primary robber as a dark leather jacket and blue jeans while the second only mentions that they fled.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "tatione",
                            "fullText": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "mary",
                            "fullText": "On MG Road when the commotion erupted. The primary robber wore a dark leather jacket. The primary robber fled and then revved a motorcycle. The primary robber headed north toward the flyover.",
                            "span": [
                                147,
                                151
                            ]
                        }
                    ]
                },
                {
                    "id": "c_6",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #7",
                    "rationale": "The first statement describes the appearance of the primary robber as wearing a dark leather jacket and blue jeans, while the second statement mentions that they revved a motorcycle.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "tatione",
                            "fullText": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "oad ",
                            "fullText": "On MG Road when the commotion erupted. The primary robber wore a dark leather jacket. The primary robber fled and then revved a motorcycle. The primary robber headed north toward the flyover.",
                            "span": [
                                7,
                                11
                            ]
                        }
                    ]
                },
                {
                    "id": "c_7",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #8",
                    "rationale": "The first statement specifies that the primary robber wore a dark leather jacket and blue jeans, while the second statement does not mention any clothing details.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "tatione",
                            "fullText": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "On MG Road when the commotion erupted. The primary",
                            "fullText": "On MG Road when the commotion erupted. The primary robber wore a dark leather jacket. The primary robber fled and then revved a motorcycle. The primary robber headed north toward the flyover.",
                            "span": [
                                0,
                                50
                            ]
                        }
                    ]
                },
                {
                    "id": "c_8",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #9",
                    "rationale": "The first statement specifies the attire of the primary robber as wearing a dark leather jacket and blue jeans, while the second statement only mentions that the thieves dashed without providing any details about their appearance.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "tatione",
                            "fullText": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "eves d",
                            "fullText": "I was walking along MG Road. Suddenly the thieves dashed from the store. The primary robber was wearing a bright red hoodie with beige cargo pants.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_9",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #10",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket and blue jeans while in Statement 2 they were wearing a bright red hoodie with beige cargo pants",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "tatione",
                            "fullText": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "ring a brig",
                            "fullText": "I was walking along MG Road. Suddenly the thieves dashed from the store. The primary robber was wearing a bright red hoodie with beige cargo pants.",
                            "span": [
                                99,
                                110
                            ]
                        }
                    ]
                },
                {
                    "id": "c_10",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #11",
                    "rationale": "Statement 1 describes three robbers sprinting out of a store with heavy duffel bags while Statement 2 mentions only one robber fleeing",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": "y duffel",
                            "fullText": "I run a café just across from the Tanishq store. I saw three robbers sprinted out of the store entrance carrying heavy duffel bags. Then the robbers pushed past frightened pedestrians on the sidewalk as people screamed for police assistance.",
                            "span": [
                                117,
                                125
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "mary",
                            "fullText": "On MG Road when the commotion erupted. The primary robber wore a dark leather jacket. The primary robber fled and then revved a motorcycle. The primary robber headed north toward the flyover.",
                            "span": [
                                147,
                                151
                            ]
                        }
                    ]
                },
                {
                    "id": "c_11",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #12",
                    "rationale": "Statement 1 describes robbers sprinting out of a store with heavy duffel bags while Statement 2 only mentions one robber heading somewhere",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": "y duffel",
                            "fullText": "I run a café just across from the Tanishq store. I saw three robbers sprinted out of the store entrance carrying heavy duffel bags. Then the robbers pushed past frightened pedestrians on the sidewalk as people screamed for police assistance.",
                            "span": [
                                117,
                                125
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "On MG Road when the commotion erupted. The primary",
                            "fullText": "On MG Road when the commotion erupted. The primary robber wore a dark leather jacket. The primary robber fled and then revved a motorcycle. The primary robber headed north toward the flyover.",
                            "span": [
                                0,
                                50
                            ]
                        }
                    ]
                },
                {
                    "id": "c_12",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #13",
                    "rationale": "Statement 1 describes robbers sprinting with heavy duffel bags out of a store entrance while Statement 2 states that thieves dashed without specifying their load.",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": "y duffel",
                            "fullText": "I run a café just across from the Tanishq store. I saw three robbers sprinted out of the store entrance carrying heavy duffel bags. Then the robbers pushed past frightened pedestrians on the sidewalk as people screamed for police assistance.",
                            "span": [
                                117,
                                125
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "eves d",
                            "fullText": "I was walking along MG Road. Suddenly the thieves dashed from the store. The primary robber was wearing a bright red hoodie with beige cargo pants.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_13",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #14",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket while in Statement 2 they were wearing a bright red hoodie with beige cargo pants.",
                    "claims": [
                        {
                            "witness": "Witness C",
                            "snippet": "On MG Road when the commotion erupted. The primary",
                            "fullText": "On MG Road when the commotion erupted. The primary robber wore a dark leather jacket. The primary robber fled and then revved a motorcycle. The primary robber headed north toward the flyover.",
                            "span": [
                                0,
                                50
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "ring a brig",
                            "fullText": "I was walking along MG Road. Suddenly the thieves dashed from the store. The primary robber was wearing a bright red hoodie with beige cargo pants.",
                            "span": [
                                99,
                                110
                            ]
                        }
                    ]
                },
                {
                    "id": "c_14",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #15",
                    "rationale": "The first statement specifies that the primary robber fled, while the second states that all thieves dashed.",
                    "claims": [
                        {
                            "witness": "Witness C",
                            "snippet": "mary",
                            "fullText": "On MG Road when the commotion erupted. The primary robber wore a dark leather jacket. The primary robber fled and then revved a motorcycle. The primary robber headed north toward the flyover.",
                            "span": [
                                147,
                                151
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "eves d",
                            "fullText": "I was walking along MG Road. Suddenly the thieves dashed from the store. The primary robber was wearing a bright red hoodie with beige cargo pants.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_15",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #16",
                    "rationale": "The first statement specifies that the primary robber wore a dark leather jacket and blue jeans while fleeing in the second.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "tatione",
                            "fullText": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "mary",
                            "fullText": "On MG Road when the commotion erupted. The primary robber wore a dark leather jacket. The primary robber fled and then revved a motorcycle. The primary robber headed north toward the flyover.",
                            "span": [
                                147,
                                151
                            ]
                        }
                    ]
                },
                {
                    "id": "c_16",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #17",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket and blue jeans while in Statement 2 they were wearing a bright red hoodie with beige cargo pants",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "tatione",
                            "fullText": "I was stationed by the glass doors of the Tanishq showroom on MG Road. Two masked robbers stormed inside. The robbers ordered all customers to lie flat on the floor. The primary robber was wearing a dark leather jacket and blue jeans.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "ring a brig",
                            "fullText": "I was walking along MG Road. Suddenly the thieves dashed from the store. The primary robber was wearing a bright red hoodie with beige cargo pants.",
                            "span": [
                                99,
                                110
                            ]
                        }
                    ]
                }
            ],
            "raw_entities": [
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        68,
                        75
                    ],
                    "text": "Tanishq",
                    "label": "PERSON",
                    "attributes": {},
                    "entity_cluster_id": "476de302-8874-4c1a-ad0f-ed212552f7f0"
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        88,
                        95
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "a2099759-8c31-4365-920e-e5cbe0097d88"
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        33,
                        40
                    ],
                    "text": "Tanishq",
                    "label": "PERSON",
                    "attributes": {},
                    "entity_cluster_id": "1b59833b-f6c3-4496-9a2e-5e4af9d2b5f3"
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        22,
                        29
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "2582f533-6fb2-4b53-b15a-296980225c5f"
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        20,
                        27
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "c9c972c2-7204-4821-8e0b-ce57b36c463e"
                }
            ],
            "raw_events": [
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        28,
                        41
                    ],
                    "text": "I was stationed by the glass doors of the Tanishq showroom on MG Road",
                    "subject": "I",
                    "action": "was stationed",
                    "object": "by the glass doors of the Tanishq showroom on MG Road",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        116,
                        130
                    ],
                    "text": "Two masked robbers stormed inside",
                    "subject": "Two masked robbers",
                    "action": "stormed inside",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        152,
                        159
                    ],
                    "text": "The robbers ordered all customers to lie flat on the floor",
                    "subject": "The robbers",
                    "action": "ordered",
                    "object": "all customers to lie flat on the floor",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        7,
                        14
                    ],
                    "text": "The primary robber was wearing a dark leather jacket and blue jeans",
                    "subject": "The primary robber",
                    "action": "was wearing",
                    "object": "a dark leather jacket and blue jeans",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        7,
                        10
                    ],
                    "text": "I run",
                    "subject": "I",
                    "action": "run",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        117,
                        125
                    ],
                    "text": "three robbers sprinted out of the store entrance carrying heavy duffel bags",
                    "subject": "three robbers",
                    "action": "sprinted",
                    "object": "out of the store entrance carrying heavy duffel bags",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        4,
                        14
                    ],
                    "text": "the robbers pushed past frightened pedestrians on the sidewalk as people screamed for police assistance",
                    "subject": "the robbers",
                    "action": "pushed",
                    "object": "past frightened pedestrians on the sidewalk as people screamed for police assistance",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        81,
                        88
                    ],
                    "text": "the commotion erupted",
                    "subject": "the commotion",
                    "action": "erupted",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        0,
                        50
                    ],
                    "text": "the primary robber wore a dark leather jacket",
                    "subject": "the primary robber",
                    "action": "wore",
                    "object": "a dark leather jacket",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        147,
                        151
                    ],
                    "text": "the primary robber fled",
                    "subject": "the primary robber",
                    "action": "fled",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        7,
                        11
                    ],
                    "text": "the primary robber revved a motorcycle",
                    "subject": "the primary robber",
                    "action": "revved",
                    "object": "a motorcycle",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        0,
                        50
                    ],
                    "text": "the primary robber headed",
                    "subject": "the primary robber",
                    "action": "headed",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        2,
                        13
                    ],
                    "text": "I was walking along MG Road",
                    "subject": "I",
                    "action": "was walking",
                    "object": "along MG Road",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        45,
                        51
                    ],
                    "text": "the thieves dashed",
                    "subject": "the thieves",
                    "action": "dashed",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        99,
                        110
                    ],
                    "text": "The primary robber was wearing a bright red hoodie with beige cargo pants",
                    "subject": "The primary robber",
                    "action": "was wearing",
                    "object": "a bright red hoodie with beige cargo pants",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        6,
                        14
                    ],
                    "text": "I securing the cash register",
                    "subject": "I",
                    "action": "securing",
                    "object": "the cash register",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        95,
                        99
                    ],
                    "text": "The thieves took fifty lakhs worth of diamond necklaces and luxury watches from the vault counters",
                    "subject": "The thieves",
                    "action": "took",
                    "object": "fifty lakhs worth of diamond necklaces and luxury watches from the vault counters",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        187,
                        217
                    ],
                    "text": "I emergency sirens began blaring",
                    "subject": "I",
                    "action": "emergency sirens began blaring",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                }
            ]
        },
        "inc-demo02": {
            "statements": [
                {
                    "id": "stmt_0",
                    "witness": "Witness A",
                    "text": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_1",
                    "witness": "Witness B",
                    "text": "I live above the shop. I heard drilling sounds late at night. Two men fled through the back alley carrying what looked like gold bars.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_2",
                    "witness": "Witness C",
                    "text": "I was watching from my window and saw one masked man wearing a blue hoodie. He revved a scooter before speeding away.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_3",
                    "witness": "Witness D",
                    "text": "I run a tea stall nearby. Three men, not two, ran past me toward the auto stand — the lead man had a bright orange jacket.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_4",
                    "witness": "Witness E",
                    "text": "I was the CCTV operator. The footage shows the vault door forced open at 00:13. The robbers took twelve kilograms of gold biscuits from safe #4.",
                    "status": "Processed"
                }
            ],
            "markers": [
                {
                    "id": "m_1",
                    "lat": 12.975,
                    "lng": 77.6069,
                    "label": "MG Road",
                    "witness": "Witness A",
                    "color": "blue"
                }
            ],
            "timeline": [
                {
                    "id": "ev_0",
                    "content": "I was stationed by the glass doors of the Tanishq showroom on MG Road",
                    "start": "2024-11-10T14:00:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_1",
                    "content": "Two masked robbers stormed inside",
                    "start": "2024-11-10T14:01:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_2",
                    "content": "The robbers ordered all customers to lie flat on the floor",
                    "start": "2024-11-10T14:02:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_3",
                    "content": "The primary robber was wearing a dark leather jacket and blue jeans",
                    "start": "2024-11-10T14:03:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_4",
                    "content": "I run",
                    "start": "2024-11-10T14:04:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_5",
                    "content": "three robbers sprinted out of the store entrance carrying heavy duffel bags",
                    "start": "2024-11-10T14:05:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_6",
                    "content": "the robbers pushed past frightened pedestrians on the sidewalk as people screamed for p...",
                    "start": "2024-11-10T14:06:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_7",
                    "content": "the commotion erupted",
                    "start": "2024-11-10T14:07:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_8",
                    "content": "the primary robber wore a dark leather jacket",
                    "start": "2024-11-10T14:08:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_9",
                    "content": "the primary robber fled",
                    "start": "2024-11-10T14:09:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_10",
                    "content": "the primary robber revved a motorcycle",
                    "start": "2024-11-10T14:10:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_11",
                    "content": "the primary robber headed",
                    "start": "2024-11-10T14:11:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_12",
                    "content": "I was walking along MG Road",
                    "start": "2024-11-10T14:12:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_13",
                    "content": "the thieves dashed",
                    "start": "2024-11-10T14:13:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_14",
                    "content": "The primary robber was wearing a bright red hoodie with beige cargo pants",
                    "start": "2024-11-10T14:14:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_15",
                    "content": "I securing the cash register",
                    "start": "2024-11-10T14:15:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_16",
                    "content": "The thieves took fifty lakhs worth of diamond necklaces and luxury watches from the vau...",
                    "start": "2024-11-10T14:16:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_17",
                    "content": "I emergency sirens began blaring",
                    "start": "2024-11-10T14:17:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                }
            ],
            "contradictions": [
                {
                    "id": "c_0",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #1",
                    "rationale": "The first statement specifies being stationed by glass doors of a Tanishq showroom, while the second only mentions walking along MG Road without mentioning any specific location or activity.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": " Malabar Gold",
                            "fullText": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                            "span": [
                                28,
                                41
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "run a tea s",
                            "fullText": "I run a tea stall nearby. Three men, not two, ran past me toward the auto stand — the lead man had a bright orange jacket.",
                            "span": [
                                2,
                                13
                            ]
                        }
                    ]
                },
                {
                    "id": "c_1",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #2",
                    "rationale": "Statement 1 describes two masked robbers entering a location while Statement 2 mentions three robbers sprinting out carrying duffel bags.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": " rear shutter.",
                            "fullText": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                            "span": [
                                116,
                                130
                            ]
                        },
                        {
                            "witness": "Witness B",
                            "snippet": "d like g",
                            "fullText": "I live above the shop. I heard drilling sounds late at night. Two men fled through the back alley carrying what looked like gold bars.",
                            "span": [
                                117,
                                125
                            ]
                        }
                    ]
                },
                {
                    "id": "c_2",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #3",
                    "rationale": "In Statement 1, it is stated that two masked robbers stormed inside; in contrast, Statement 2 mentions only one robber fleeing.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": " rear shutter.",
                            "fullText": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                            "span": [
                                116,
                                130
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I was watching from my window ",
                            "fullText": "I was watching from my window and saw one masked man wearing a blue hoodie. He revved a scooter before speeding away.",
                            "span": [
                                117,
                                117
                            ]
                        }
                    ]
                },
                {
                    "id": "c_3",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #4",
                    "rationale": "The first statement mentions two masked robbers storming in while the second specifies that the primary robber was revving a motorcycle.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": " rear shutter.",
                            "fullText": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                            "span": [
                                116,
                                130
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "atch",
                            "fullText": "I was watching from my window and saw one masked man wearing a blue hoodie. He revved a scooter before speeding away.",
                            "span": [
                                7,
                                11
                            ]
                        }
                    ]
                },
                {
                    "id": "c_4",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #5",
                    "rationale": "The primary robber in Statement 1 was described as wearing a dark leather jacket and blue jeans, while Statement 2 mentions three robbers sprinting out of the store entrance carrying heavy duffel bags without specifying attire.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he nigh",
                            "fullText": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness B",
                            "snippet": "d like g",
                            "fullText": "I live above the shop. I heard drilling sounds late at night. Two men fled through the back alley carrying what looked like gold bars.",
                            "span": [
                                117,
                                125
                            ]
                        }
                    ]
                },
                {
                    "id": "c_5",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #6",
                    "rationale": "The first statement specifies the attire of the primary robber as a dark leather jacket and blue jeans while the second only mentions that they fled.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he nigh",
                            "fullText": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I was watching from my window ",
                            "fullText": "I was watching from my window and saw one masked man wearing a blue hoodie. He revved a scooter before speeding away.",
                            "span": [
                                117,
                                117
                            ]
                        }
                    ]
                },
                {
                    "id": "c_6",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #7",
                    "rationale": "The first statement describes the appearance of the primary robber as wearing a dark leather jacket and blue jeans, while the second statement mentions that they revved a motorcycle.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he nigh",
                            "fullText": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "atch",
                            "fullText": "I was watching from my window and saw one masked man wearing a blue hoodie. He revved a scooter before speeding away.",
                            "span": [
                                7,
                                11
                            ]
                        }
                    ]
                },
                {
                    "id": "c_7",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #8",
                    "rationale": "The first statement specifies that the primary robber wore a dark leather jacket and blue jeans, while the second statement does not mention any clothing details.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he nigh",
                            "fullText": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I was watching from my window and saw one masked m",
                            "fullText": "I was watching from my window and saw one masked man wearing a blue hoodie. He revved a scooter before speeding away.",
                            "span": [
                                0,
                                50
                            ]
                        }
                    ]
                },
                {
                    "id": "c_8",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #9",
                    "rationale": "The first statement specifies the attire of the primary robber as wearing a dark leather jacket and blue jeans, while the second statement only mentions that the thieves dashed without providing any details about their appearance.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he nigh",
                            "fullText": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": " ran p",
                            "fullText": "I run a tea stall nearby. Three men, not two, ran past me toward the auto stand — the lead man had a bright orange jacket.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_9",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #10",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket and blue jeans while in Statement 2 they were wearing a bright red hoodie with beige cargo pants",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he nigh",
                            "fullText": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "a bright or",
                            "fullText": "I run a tea stall nearby. Three men, not two, ran past me toward the auto stand — the lead man had a bright orange jacket.",
                            "span": [
                                99,
                                110
                            ]
                        }
                    ]
                },
                {
                    "id": "c_10",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #11",
                    "rationale": "Statement 1 describes three robbers sprinting out of a store with heavy duffel bags while Statement 2 mentions only one robber fleeing",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": "d like g",
                            "fullText": "I live above the shop. I heard drilling sounds late at night. Two men fled through the back alley carrying what looked like gold bars.",
                            "span": [
                                117,
                                125
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I was watching from my window ",
                            "fullText": "I was watching from my window and saw one masked man wearing a blue hoodie. He revved a scooter before speeding away.",
                            "span": [
                                117,
                                117
                            ]
                        }
                    ]
                },
                {
                    "id": "c_11",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #12",
                    "rationale": "Statement 1 describes robbers sprinting out of a store with heavy duffel bags while Statement 2 only mentions one robber heading somewhere",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": "d like g",
                            "fullText": "I live above the shop. I heard drilling sounds late at night. Two men fled through the back alley carrying what looked like gold bars.",
                            "span": [
                                117,
                                125
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I was watching from my window and saw one masked m",
                            "fullText": "I was watching from my window and saw one masked man wearing a blue hoodie. He revved a scooter before speeding away.",
                            "span": [
                                0,
                                50
                            ]
                        }
                    ]
                },
                {
                    "id": "c_12",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #13",
                    "rationale": "Statement 1 describes robbers sprinting with heavy duffel bags out of a store entrance while Statement 2 states that thieves dashed without specifying their load.",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": "d like g",
                            "fullText": "I live above the shop. I heard drilling sounds late at night. Two men fled through the back alley carrying what looked like gold bars.",
                            "span": [
                                117,
                                125
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": " ran p",
                            "fullText": "I run a tea stall nearby. Three men, not two, ran past me toward the auto stand — the lead man had a bright orange jacket.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_13",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #14",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket while in Statement 2 they were wearing a bright red hoodie with beige cargo pants.",
                    "claims": [
                        {
                            "witness": "Witness C",
                            "snippet": "I was watching from my window and saw one masked m",
                            "fullText": "I was watching from my window and saw one masked man wearing a blue hoodie. He revved a scooter before speeding away.",
                            "span": [
                                0,
                                50
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "a bright or",
                            "fullText": "I run a tea stall nearby. Three men, not two, ran past me toward the auto stand — the lead man had a bright orange jacket.",
                            "span": [
                                99,
                                110
                            ]
                        }
                    ]
                },
                {
                    "id": "c_14",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #15",
                    "rationale": "The first statement specifies that the primary robber fled, while the second states that all thieves dashed.",
                    "claims": [
                        {
                            "witness": "Witness C",
                            "snippet": "I was watching from my window ",
                            "fullText": "I was watching from my window and saw one masked man wearing a blue hoodie. He revved a scooter before speeding away.",
                            "span": [
                                117,
                                117
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": " ran p",
                            "fullText": "I run a tea stall nearby. Three men, not two, ran past me toward the auto stand — the lead man had a bright orange jacket.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_15",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #16",
                    "rationale": "The first statement specifies that the primary robber wore a dark leather jacket and blue jeans while fleeing in the second.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he nigh",
                            "fullText": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I was watching from my window ",
                            "fullText": "I was watching from my window and saw one masked man wearing a blue hoodie. He revved a scooter before speeding away.",
                            "span": [
                                117,
                                117
                            ]
                        }
                    ]
                },
                {
                    "id": "c_16",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #17",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket and blue jeans while in Statement 2 they were wearing a bright red hoodie with beige cargo pants",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he nigh",
                            "fullText": "I was the night guard at the Malabar Gold vault on Commercial Street. Around midnight two masked men cut through the rear shutter.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "a bright or",
                            "fullText": "I run a tea stall nearby. Three men, not two, ran past me toward the auto stand — the lead man had a bright orange jacket.",
                            "span": [
                                99,
                                110
                            ]
                        }
                    ]
                }
            ],
            "raw_entities": [
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        68,
                        75
                    ],
                    "text": "Tanishq",
                    "label": "PERSON",
                    "attributes": {},
                    "entity_cluster_id": "476de302-8874-4c1a-ad0f-ed212552f7f0"
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        88,
                        95
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "a2099759-8c31-4365-920e-e5cbe0097d88"
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        33,
                        40
                    ],
                    "text": "Tanishq",
                    "label": "PERSON",
                    "attributes": {},
                    "entity_cluster_id": "1b59833b-f6c3-4496-9a2e-5e4af9d2b5f3"
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        22,
                        29
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "2582f533-6fb2-4b53-b15a-296980225c5f"
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        20,
                        27
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "c9c972c2-7204-4821-8e0b-ce57b36c463e"
                }
            ],
            "raw_events": [
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        28,
                        41
                    ],
                    "text": "I was stationed by the glass doors of the Tanishq showroom on MG Road",
                    "subject": "I",
                    "action": "was stationed",
                    "object": "by the glass doors of the Tanishq showroom on MG Road",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        116,
                        130
                    ],
                    "text": "Two masked robbers stormed inside",
                    "subject": "Two masked robbers",
                    "action": "stormed inside",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        152,
                        159
                    ],
                    "text": "The robbers ordered all customers to lie flat on the floor",
                    "subject": "The robbers",
                    "action": "ordered",
                    "object": "all customers to lie flat on the floor",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        7,
                        14
                    ],
                    "text": "The primary robber was wearing a dark leather jacket and blue jeans",
                    "subject": "The primary robber",
                    "action": "was wearing",
                    "object": "a dark leather jacket and blue jeans",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        7,
                        10
                    ],
                    "text": "I run",
                    "subject": "I",
                    "action": "run",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        117,
                        125
                    ],
                    "text": "three robbers sprinted out of the store entrance carrying heavy duffel bags",
                    "subject": "three robbers",
                    "action": "sprinted",
                    "object": "out of the store entrance carrying heavy duffel bags",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        4,
                        14
                    ],
                    "text": "the robbers pushed past frightened pedestrians on the sidewalk as people screamed for police assistance",
                    "subject": "the robbers",
                    "action": "pushed",
                    "object": "past frightened pedestrians on the sidewalk as people screamed for police assistance",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        81,
                        88
                    ],
                    "text": "the commotion erupted",
                    "subject": "the commotion",
                    "action": "erupted",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        0,
                        50
                    ],
                    "text": "the primary robber wore a dark leather jacket",
                    "subject": "the primary robber",
                    "action": "wore",
                    "object": "a dark leather jacket",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        147,
                        151
                    ],
                    "text": "the primary robber fled",
                    "subject": "the primary robber",
                    "action": "fled",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        7,
                        11
                    ],
                    "text": "the primary robber revved a motorcycle",
                    "subject": "the primary robber",
                    "action": "revved",
                    "object": "a motorcycle",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        0,
                        50
                    ],
                    "text": "the primary robber headed",
                    "subject": "the primary robber",
                    "action": "headed",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        2,
                        13
                    ],
                    "text": "I was walking along MG Road",
                    "subject": "I",
                    "action": "was walking",
                    "object": "along MG Road",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        45,
                        51
                    ],
                    "text": "the thieves dashed",
                    "subject": "the thieves",
                    "action": "dashed",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        99,
                        110
                    ],
                    "text": "The primary robber was wearing a bright red hoodie with beige cargo pants",
                    "subject": "The primary robber",
                    "action": "was wearing",
                    "object": "a bright red hoodie with beige cargo pants",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        6,
                        14
                    ],
                    "text": "I securing the cash register",
                    "subject": "I",
                    "action": "securing",
                    "object": "the cash register",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        95,
                        99
                    ],
                    "text": "The thieves took fifty lakhs worth of diamond necklaces and luxury watches from the vault counters",
                    "subject": "The thieves",
                    "action": "took",
                    "object": "fifty lakhs worth of diamond necklaces and luxury watches from the vault counters",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        187,
                        217
                    ],
                    "text": "I emergency sirens began blaring",
                    "subject": "I",
                    "action": "emergency sirens began blaring",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                }
            ]
        },
        "inc-demo03": {
            "statements": [
                {
                    "id": "stmt_0",
                    "witness": "Witness A",
                    "text": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_1",
                    "witness": "Witness B",
                    "text": "I was passing by in an auto when I saw two men prying open the ATM. They escaped in a white sedan towards the 100 Feet Road.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_2",
                    "witness": "Witness C",
                    "text": "I live across the street. The vehicle was black — definitely an SUV, not a sedan. One of the men was wearing a red jacket.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_3",
                    "witness": "Witness D",
                    "text": "I am the bank branch manager. CCTV confirmed the incident at 01:07. Two crore rupees in cash was removed from the ATM cassettes.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_4",
                    "witness": "Witness E",
                    "text": "I witnessed the getaway from the adjacent parking lot. The car was silver — I am certain because it passed under the street light.",
                    "status": "Processed"
                }
            ],
            "markers": [
                {
                    "id": "m_1",
                    "lat": 12.975,
                    "lng": 77.6069,
                    "label": "MG Road",
                    "witness": "Witness A",
                    "color": "blue"
                }
            ],
            "timeline": [
                {
                    "id": "ev_0",
                    "content": "I was stationed by the glass doors of the Tanishq showroom on MG Road",
                    "start": "2024-10-22T14:00:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_1",
                    "content": "Two masked robbers stormed inside",
                    "start": "2024-10-22T14:01:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_2",
                    "content": "The robbers ordered all customers to lie flat on the floor",
                    "start": "2024-10-22T14:02:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_3",
                    "content": "The primary robber was wearing a dark leather jacket and blue jeans",
                    "start": "2024-10-22T14:03:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_4",
                    "content": "I run",
                    "start": "2024-10-22T14:04:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_5",
                    "content": "three robbers sprinted out of the store entrance carrying heavy duffel bags",
                    "start": "2024-10-22T14:05:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_6",
                    "content": "the robbers pushed past frightened pedestrians on the sidewalk as people screamed for p...",
                    "start": "2024-10-22T14:06:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_7",
                    "content": "the commotion erupted",
                    "start": "2024-10-22T14:07:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_8",
                    "content": "the primary robber wore a dark leather jacket",
                    "start": "2024-10-22T14:08:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_9",
                    "content": "the primary robber fled",
                    "start": "2024-10-22T14:09:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_10",
                    "content": "the primary robber revved a motorcycle",
                    "start": "2024-10-22T14:10:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_11",
                    "content": "the primary robber headed",
                    "start": "2024-10-22T14:11:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_12",
                    "content": "I was walking along MG Road",
                    "start": "2024-10-22T14:12:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_13",
                    "content": "the thieves dashed",
                    "start": "2024-10-22T14:13:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_14",
                    "content": "The primary robber was wearing a bright red hoodie with beige cargo pants",
                    "start": "2024-10-22T14:14:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_15",
                    "content": "I securing the cash register",
                    "start": "2024-10-22T14:15:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_16",
                    "content": "The thieves took fifty lakhs worth of diamond necklaces and luxury watches from the vau...",
                    "start": "2024-10-22T14:16:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_17",
                    "content": "I emergency sirens began blaring",
                    "start": "2024-10-22T14:17:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                }
            ],
            "contradictions": [
                {
                    "id": "c_0",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #1",
                    "rationale": "The first statement specifies being stationed by glass doors of a Tanishq showroom, while the second only mentions walking along MG Road without mentioning any specific location or activity.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": " on duty. At ",
                            "fullText": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                            "span": [
                                28,
                                41
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "am the bank",
                            "fullText": "I am the bank branch manager. CCTV confirmed the incident at 01:07. Two crore rupees in cash was removed from the ATM cassettes.",
                            "span": [
                                2,
                                13
                            ]
                        }
                    ]
                },
                {
                    "id": "c_1",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #2",
                    "rationale": "Statement 1 describes two masked robbers entering a location while Statement 2 mentions three robbers sprinting out carrying duffel bags.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "t with hydraul",
                            "fullText": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                            "span": [
                                116,
                                130
                            ]
                        },
                        {
                            "witness": "Witness B",
                            "snippet": "t Road.",
                            "fullText": "I was passing by in an auto when I saw two men prying open the ATM. They escaped in a white sedan towards the 100 Feet Road.",
                            "span": [
                                117,
                                124
                            ]
                        }
                    ]
                },
                {
                    "id": "c_2",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #3",
                    "rationale": "In Statement 1, it is stated that two masked robbers stormed inside; in contrast, Statement 2 mentions only one robber fleeing.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "t with hydraul",
                            "fullText": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                            "span": [
                                116,
                                130
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I live across the street. The ",
                            "fullText": "I live across the street. The vehicle was black — definitely an SUV, not a sedan. One of the men was wearing a red jacket.",
                            "span": [
                                122,
                                122
                            ]
                        }
                    ]
                },
                {
                    "id": "c_3",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #4",
                    "rationale": "The first statement mentions two masked robbers storming in while the second specifies that the primary robber was revving a motorcycle.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "t with hydraul",
                            "fullText": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                            "span": [
                                116,
                                130
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "acro",
                            "fullText": "I live across the street. The vehicle was black — definitely an SUV, not a sedan. One of the men was wearing a red jacket.",
                            "span": [
                                7,
                                11
                            ]
                        }
                    ]
                },
                {
                    "id": "c_4",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #5",
                    "rationale": "The primary robber in Statement 1 was described as wearing a dark leather jacket and blue jeans, while Statement 2 mentions three robbers sprinting out of the store entrance carrying heavy duffel bags without specifying attire.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he ATM ",
                            "fullText": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness B",
                            "snippet": "t Road.",
                            "fullText": "I was passing by in an auto when I saw two men prying open the ATM. They escaped in a white sedan towards the 100 Feet Road.",
                            "span": [
                                117,
                                124
                            ]
                        }
                    ]
                },
                {
                    "id": "c_5",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #6",
                    "rationale": "The first statement specifies the attire of the primary robber as a dark leather jacket and blue jeans while the second only mentions that they fled.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he ATM ",
                            "fullText": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I live across the street. The ",
                            "fullText": "I live across the street. The vehicle was black — definitely an SUV, not a sedan. One of the men was wearing a red jacket.",
                            "span": [
                                122,
                                122
                            ]
                        }
                    ]
                },
                {
                    "id": "c_6",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #7",
                    "rationale": "The first statement describes the appearance of the primary robber as wearing a dark leather jacket and blue jeans, while the second statement mentions that they revved a motorcycle.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he ATM ",
                            "fullText": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "acro",
                            "fullText": "I live across the street. The vehicle was black — definitely an SUV, not a sedan. One of the men was wearing a red jacket.",
                            "span": [
                                7,
                                11
                            ]
                        }
                    ]
                },
                {
                    "id": "c_7",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #8",
                    "rationale": "The first statement specifies that the primary robber wore a dark leather jacket and blue jeans, while the second statement does not mention any clothing details.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he ATM ",
                            "fullText": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I live across the street. The vehicle was black — ",
                            "fullText": "I live across the street. The vehicle was black — definitely an SUV, not a sedan. One of the men was wearing a red jacket.",
                            "span": [
                                0,
                                50
                            ]
                        }
                    ]
                },
                {
                    "id": "c_8",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #9",
                    "rationale": "The first statement specifies the attire of the primary robber as wearing a dark leather jacket and blue jeans, while the second statement only mentions that the thieves dashed without providing any details about their appearance.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he ATM ",
                            "fullText": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "the in",
                            "fullText": "I am the bank branch manager. CCTV confirmed the incident at 01:07. Two crore rupees in cash was removed from the ATM cassettes.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_9",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #10",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket and blue jeans while in Statement 2 they were wearing a bright red hoodie with beige cargo pants",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he ATM ",
                            "fullText": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "moved from ",
                            "fullText": "I am the bank branch manager. CCTV confirmed the incident at 01:07. Two crore rupees in cash was removed from the ATM cassettes.",
                            "span": [
                                99,
                                110
                            ]
                        }
                    ]
                },
                {
                    "id": "c_10",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #11",
                    "rationale": "Statement 1 describes three robbers sprinting out of a store with heavy duffel bags while Statement 2 mentions only one robber fleeing",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": "t Road.",
                            "fullText": "I was passing by in an auto when I saw two men prying open the ATM. They escaped in a white sedan towards the 100 Feet Road.",
                            "span": [
                                117,
                                124
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I live across the street. The ",
                            "fullText": "I live across the street. The vehicle was black — definitely an SUV, not a sedan. One of the men was wearing a red jacket.",
                            "span": [
                                122,
                                122
                            ]
                        }
                    ]
                },
                {
                    "id": "c_11",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #12",
                    "rationale": "Statement 1 describes robbers sprinting out of a store with heavy duffel bags while Statement 2 only mentions one robber heading somewhere",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": "t Road.",
                            "fullText": "I was passing by in an auto when I saw two men prying open the ATM. They escaped in a white sedan towards the 100 Feet Road.",
                            "span": [
                                117,
                                124
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I live across the street. The vehicle was black — ",
                            "fullText": "I live across the street. The vehicle was black — definitely an SUV, not a sedan. One of the men was wearing a red jacket.",
                            "span": [
                                0,
                                50
                            ]
                        }
                    ]
                },
                {
                    "id": "c_12",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #13",
                    "rationale": "Statement 1 describes robbers sprinting with heavy duffel bags out of a store entrance while Statement 2 states that thieves dashed without specifying their load.",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": "t Road.",
                            "fullText": "I was passing by in an auto when I saw two men prying open the ATM. They escaped in a white sedan towards the 100 Feet Road.",
                            "span": [
                                117,
                                124
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "the in",
                            "fullText": "I am the bank branch manager. CCTV confirmed the incident at 01:07. Two crore rupees in cash was removed from the ATM cassettes.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_13",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #14",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket while in Statement 2 they were wearing a bright red hoodie with beige cargo pants.",
                    "claims": [
                        {
                            "witness": "Witness C",
                            "snippet": "I live across the street. The vehicle was black — ",
                            "fullText": "I live across the street. The vehicle was black — definitely an SUV, not a sedan. One of the men was wearing a red jacket.",
                            "span": [
                                0,
                                50
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "moved from ",
                            "fullText": "I am the bank branch manager. CCTV confirmed the incident at 01:07. Two crore rupees in cash was removed from the ATM cassettes.",
                            "span": [
                                99,
                                110
                            ]
                        }
                    ]
                },
                {
                    "id": "c_14",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #15",
                    "rationale": "The first statement specifies that the primary robber fled, while the second states that all thieves dashed.",
                    "claims": [
                        {
                            "witness": "Witness C",
                            "snippet": "I live across the street. The ",
                            "fullText": "I live across the street. The vehicle was black — definitely an SUV, not a sedan. One of the men was wearing a red jacket.",
                            "span": [
                                122,
                                122
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "the in",
                            "fullText": "I am the bank branch manager. CCTV confirmed the incident at 01:07. Two crore rupees in cash was removed from the ATM cassettes.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_15",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #16",
                    "rationale": "The first statement specifies that the primary robber wore a dark leather jacket and blue jeans while fleeing in the second.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he ATM ",
                            "fullText": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I live across the street. The ",
                            "fullText": "I live across the street. The vehicle was black — definitely an SUV, not a sedan. One of the men was wearing a red jacket.",
                            "span": [
                                122,
                                122
                            ]
                        }
                    ]
                },
                {
                    "id": "c_16",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #17",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket and blue jeans while in Statement 2 they were wearing a bright red hoodie with beige cargo pants",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "he ATM ",
                            "fullText": "I was the ATM security guard on duty. At approximately 1 AM a black SUV rammed the ATM kiosk and three men jumped out with hydraulic cutters.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "moved from ",
                            "fullText": "I am the bank branch manager. CCTV confirmed the incident at 01:07. Two crore rupees in cash was removed from the ATM cassettes.",
                            "span": [
                                99,
                                110
                            ]
                        }
                    ]
                }
            ],
            "raw_entities": [
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        68,
                        75
                    ],
                    "text": "Tanishq",
                    "label": "PERSON",
                    "attributes": {},
                    "entity_cluster_id": "476de302-8874-4c1a-ad0f-ed212552f7f0"
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        88,
                        95
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "a2099759-8c31-4365-920e-e5cbe0097d88"
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        33,
                        40
                    ],
                    "text": "Tanishq",
                    "label": "PERSON",
                    "attributes": {},
                    "entity_cluster_id": "1b59833b-f6c3-4496-9a2e-5e4af9d2b5f3"
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        22,
                        29
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "2582f533-6fb2-4b53-b15a-296980225c5f"
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        20,
                        27
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "c9c972c2-7204-4821-8e0b-ce57b36c463e"
                }
            ],
            "raw_events": [
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        28,
                        41
                    ],
                    "text": "I was stationed by the glass doors of the Tanishq showroom on MG Road",
                    "subject": "I",
                    "action": "was stationed",
                    "object": "by the glass doors of the Tanishq showroom on MG Road",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        116,
                        130
                    ],
                    "text": "Two masked robbers stormed inside",
                    "subject": "Two masked robbers",
                    "action": "stormed inside",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        152,
                        159
                    ],
                    "text": "The robbers ordered all customers to lie flat on the floor",
                    "subject": "The robbers",
                    "action": "ordered",
                    "object": "all customers to lie flat on the floor",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        7,
                        14
                    ],
                    "text": "The primary robber was wearing a dark leather jacket and blue jeans",
                    "subject": "The primary robber",
                    "action": "was wearing",
                    "object": "a dark leather jacket and blue jeans",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        7,
                        10
                    ],
                    "text": "I run",
                    "subject": "I",
                    "action": "run",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        117,
                        125
                    ],
                    "text": "three robbers sprinted out of the store entrance carrying heavy duffel bags",
                    "subject": "three robbers",
                    "action": "sprinted",
                    "object": "out of the store entrance carrying heavy duffel bags",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        4,
                        14
                    ],
                    "text": "the robbers pushed past frightened pedestrians on the sidewalk as people screamed for police assistance",
                    "subject": "the robbers",
                    "action": "pushed",
                    "object": "past frightened pedestrians on the sidewalk as people screamed for police assistance",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        81,
                        88
                    ],
                    "text": "the commotion erupted",
                    "subject": "the commotion",
                    "action": "erupted",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        0,
                        50
                    ],
                    "text": "the primary robber wore a dark leather jacket",
                    "subject": "the primary robber",
                    "action": "wore",
                    "object": "a dark leather jacket",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        147,
                        151
                    ],
                    "text": "the primary robber fled",
                    "subject": "the primary robber",
                    "action": "fled",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        7,
                        11
                    ],
                    "text": "the primary robber revved a motorcycle",
                    "subject": "the primary robber",
                    "action": "revved",
                    "object": "a motorcycle",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        0,
                        50
                    ],
                    "text": "the primary robber headed",
                    "subject": "the primary robber",
                    "action": "headed",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        2,
                        13
                    ],
                    "text": "I was walking along MG Road",
                    "subject": "I",
                    "action": "was walking",
                    "object": "along MG Road",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        45,
                        51
                    ],
                    "text": "the thieves dashed",
                    "subject": "the thieves",
                    "action": "dashed",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        99,
                        110
                    ],
                    "text": "The primary robber was wearing a bright red hoodie with beige cargo pants",
                    "subject": "The primary robber",
                    "action": "was wearing",
                    "object": "a bright red hoodie with beige cargo pants",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        6,
                        14
                    ],
                    "text": "I securing the cash register",
                    "subject": "I",
                    "action": "securing",
                    "object": "the cash register",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        95,
                        99
                    ],
                    "text": "The thieves took fifty lakhs worth of diamond necklaces and luxury watches from the vault counters",
                    "subject": "The thieves",
                    "action": "took",
                    "object": "fifty lakhs worth of diamond necklaces and luxury watches from the vault counters",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        187,
                        217
                    ],
                    "text": "I emergency sirens began blaring",
                    "subject": "I",
                    "action": "emergency sirens began blaring",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                }
            ]
        },
        "inc-demo04": {
            "statements": [
                {
                    "id": "stmt_0",
                    "witness": "Witness A",
                    "text": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_1",
                    "witness": "Witness B",
                    "text": "I was a customer inside the shop. I saw three robbers — one stayed at the door, two went behind the counter.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_2",
                    "witness": "Witness C",
                    "text": "I am a vendor next door. I heard shouting and saw one man run out without a weapon. He wore a grey tracksuit.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_3",
                    "witness": "Witness D",
                    "text": "I was on the street opposite. The man I saw fleeing wore a black kurta, not a tracksuit.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_4",
                    "witness": "Witness E",
                    "text": "I am the investigating officer. Forensics confirmed two distinct sets of boot prints inside. Witness accounts conflict on the number of robbers — two vs three.",
                    "status": "Processed"
                }
            ],
            "markers": [
                {
                    "id": "m_1",
                    "lat": 12.975,
                    "lng": 77.6069,
                    "label": "MG Road",
                    "witness": "Witness A",
                    "color": "blue"
                }
            ],
            "timeline": [
                {
                    "id": "ev_0",
                    "content": "I was stationed by the glass doors of the Tanishq showroom on MG Road",
                    "start": "2024-09-14T14:00:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_1",
                    "content": "Two masked robbers stormed inside",
                    "start": "2024-09-14T14:01:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_2",
                    "content": "The robbers ordered all customers to lie flat on the floor",
                    "start": "2024-09-14T14:02:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_3",
                    "content": "The primary robber was wearing a dark leather jacket and blue jeans",
                    "start": "2024-09-14T14:03:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_4",
                    "content": "I run",
                    "start": "2024-09-14T14:04:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_5",
                    "content": "three robbers sprinted out of the store entrance carrying heavy duffel bags",
                    "start": "2024-09-14T14:05:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_6",
                    "content": "the robbers pushed past frightened pedestrians on the sidewalk as people screamed for p...",
                    "start": "2024-09-14T14:06:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_7",
                    "content": "the commotion erupted",
                    "start": "2024-09-14T14:07:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_8",
                    "content": "the primary robber wore a dark leather jacket",
                    "start": "2024-09-14T14:08:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_9",
                    "content": "the primary robber fled",
                    "start": "2024-09-14T14:09:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_10",
                    "content": "the primary robber revved a motorcycle",
                    "start": "2024-09-14T14:10:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_11",
                    "content": "the primary robber headed",
                    "start": "2024-09-14T14:11:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_12",
                    "content": "I was walking along MG Road",
                    "start": "2024-09-14T14:12:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_13",
                    "content": "the thieves dashed",
                    "start": "2024-09-14T14:13:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_14",
                    "content": "The primary robber was wearing a bright red hoodie with beige cargo pants",
                    "start": "2024-09-14T14:14:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_15",
                    "content": "I securing the cash register",
                    "start": "2024-09-14T14:15:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_16",
                    "content": "The thieves took fifty lakhs worth of diamond necklaces and luxury watches from the vau...",
                    "start": "2024-09-14T14:16:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_17",
                    "content": "I emergency sirens began blaring",
                    "start": "2024-09-14T14:17:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                }
            ],
            "contradictions": [
                {
                    "id": "c_0",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #1",
                    "rationale": "The first statement specifies being stationed by glass doors of a Tanishq showroom, while the second only mentions walking along MG Road without mentioning any specific location or activity.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "ed men walked",
                            "fullText": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                            "span": [
                                28,
                                41
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "was on the ",
                            "fullText": "I was on the street opposite. The man I saw fleeing wore a black kurta, not a tracksuit.",
                            "span": [
                                2,
                                13
                            ]
                        }
                    ]
                },
                {
                    "id": "c_1",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #2",
                    "rationale": "Statement 1 describes two masked robbers entering a location while Statement 2 mentions three robbers sprinting out carrying duffel bags.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "h eighty lakhs",
                            "fullText": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                            "span": [
                                116,
                                130
                            ]
                        },
                        {
                            "witness": "Witness B",
                            "snippet": "I was a customer inside the sh",
                            "fullText": "I was a customer inside the shop. I saw three robbers — one stayed at the door, two went behind the counter.",
                            "span": [
                                108,
                                108
                            ]
                        }
                    ]
                },
                {
                    "id": "c_2",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #3",
                    "rationale": "In Statement 1, it is stated that two masked robbers stormed inside; in contrast, Statement 2 mentions only one robber fleeing.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "h eighty lakhs",
                            "fullText": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                            "span": [
                                116,
                                130
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I am a vendor next door. I hea",
                            "fullText": "I am a vendor next door. I heard shouting and saw one man run out without a weapon. He wore a grey tracksuit.",
                            "span": [
                                109,
                                109
                            ]
                        }
                    ]
                },
                {
                    "id": "c_3",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #4",
                    "rationale": "The first statement mentions two masked robbers storming in while the second specifies that the primary robber was revving a motorcycle.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "h eighty lakhs",
                            "fullText": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                            "span": [
                                116,
                                130
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "vend",
                            "fullText": "I am a vendor next door. I heard shouting and saw one man run out without a weapon. He wore a grey tracksuit.",
                            "span": [
                                7,
                                11
                            ]
                        }
                    ]
                },
                {
                    "id": "c_4",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #5",
                    "rationale": "The primary robber in Statement 1 was described as wearing a dark leather jacket and blue jeans, while Statement 2 mentions three robbers sprinting out of the store entrance carrying heavy duffel bags without specifying attire.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e shop ",
                            "fullText": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness B",
                            "snippet": "I was a customer inside the sh",
                            "fullText": "I was a customer inside the shop. I saw three robbers — one stayed at the door, two went behind the counter.",
                            "span": [
                                108,
                                108
                            ]
                        }
                    ]
                },
                {
                    "id": "c_5",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #6",
                    "rationale": "The first statement specifies the attire of the primary robber as a dark leather jacket and blue jeans while the second only mentions that they fled.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e shop ",
                            "fullText": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I am a vendor next door. I hea",
                            "fullText": "I am a vendor next door. I heard shouting and saw one man run out without a weapon. He wore a grey tracksuit.",
                            "span": [
                                109,
                                109
                            ]
                        }
                    ]
                },
                {
                    "id": "c_6",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #7",
                    "rationale": "The first statement describes the appearance of the primary robber as wearing a dark leather jacket and blue jeans, while the second statement mentions that they revved a motorcycle.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e shop ",
                            "fullText": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "vend",
                            "fullText": "I am a vendor next door. I heard shouting and saw one man run out without a weapon. He wore a grey tracksuit.",
                            "span": [
                                7,
                                11
                            ]
                        }
                    ]
                },
                {
                    "id": "c_7",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #8",
                    "rationale": "The first statement specifies that the primary robber wore a dark leather jacket and blue jeans, while the second statement does not mention any clothing details.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e shop ",
                            "fullText": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I am a vendor next door. I heard shouting and saw ",
                            "fullText": "I am a vendor next door. I heard shouting and saw one man run out without a weapon. He wore a grey tracksuit.",
                            "span": [
                                0,
                                50
                            ]
                        }
                    ]
                },
                {
                    "id": "c_8",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #9",
                    "rationale": "The first statement specifies the attire of the primary robber as wearing a dark leather jacket and blue jeans, while the second statement only mentions that the thieves dashed without providing any details about their appearance.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e shop ",
                            "fullText": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "leeing",
                            "fullText": "I was on the street opposite. The man I saw fleeing wore a black kurta, not a tracksuit.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_9",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #10",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket and blue jeans while in Statement 2 they were wearing a bright red hoodie with beige cargo pants",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e shop ",
                            "fullText": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "I was on the street opposite. ",
                            "fullText": "I was on the street opposite. The man I saw fleeing wore a black kurta, not a tracksuit.",
                            "span": [
                                88,
                                88
                            ]
                        }
                    ]
                },
                {
                    "id": "c_10",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #11",
                    "rationale": "Statement 1 describes three robbers sprinting out of a store with heavy duffel bags while Statement 2 mentions only one robber fleeing",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": "I was a customer inside the sh",
                            "fullText": "I was a customer inside the shop. I saw three robbers — one stayed at the door, two went behind the counter.",
                            "span": [
                                108,
                                108
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I am a vendor next door. I hea",
                            "fullText": "I am a vendor next door. I heard shouting and saw one man run out without a weapon. He wore a grey tracksuit.",
                            "span": [
                                109,
                                109
                            ]
                        }
                    ]
                },
                {
                    "id": "c_11",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #12",
                    "rationale": "Statement 1 describes robbers sprinting out of a store with heavy duffel bags while Statement 2 only mentions one robber heading somewhere",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": "I was a customer inside the sh",
                            "fullText": "I was a customer inside the shop. I saw three robbers — one stayed at the door, two went behind the counter.",
                            "span": [
                                108,
                                108
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I am a vendor next door. I heard shouting and saw ",
                            "fullText": "I am a vendor next door. I heard shouting and saw one man run out without a weapon. He wore a grey tracksuit.",
                            "span": [
                                0,
                                50
                            ]
                        }
                    ]
                },
                {
                    "id": "c_12",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #13",
                    "rationale": "Statement 1 describes robbers sprinting with heavy duffel bags out of a store entrance while Statement 2 states that thieves dashed without specifying their load.",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": "I was a customer inside the sh",
                            "fullText": "I was a customer inside the shop. I saw three robbers — one stayed at the door, two went behind the counter.",
                            "span": [
                                108,
                                108
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "leeing",
                            "fullText": "I was on the street opposite. The man I saw fleeing wore a black kurta, not a tracksuit.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_13",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #14",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket while in Statement 2 they were wearing a bright red hoodie with beige cargo pants.",
                    "claims": [
                        {
                            "witness": "Witness C",
                            "snippet": "I am a vendor next door. I heard shouting and saw ",
                            "fullText": "I am a vendor next door. I heard shouting and saw one man run out without a weapon. He wore a grey tracksuit.",
                            "span": [
                                0,
                                50
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "I was on the street opposite. ",
                            "fullText": "I was on the street opposite. The man I saw fleeing wore a black kurta, not a tracksuit.",
                            "span": [
                                88,
                                88
                            ]
                        }
                    ]
                },
                {
                    "id": "c_14",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #15",
                    "rationale": "The first statement specifies that the primary robber fled, while the second states that all thieves dashed.",
                    "claims": [
                        {
                            "witness": "Witness C",
                            "snippet": "I am a vendor next door. I hea",
                            "fullText": "I am a vendor next door. I heard shouting and saw one man run out without a weapon. He wore a grey tracksuit.",
                            "span": [
                                109,
                                109
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "leeing",
                            "fullText": "I was on the street opposite. The man I saw fleeing wore a black kurta, not a tracksuit.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_15",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #16",
                    "rationale": "The first statement specifies that the primary robber wore a dark leather jacket and blue jeans while fleeing in the second.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e shop ",
                            "fullText": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I am a vendor next door. I hea",
                            "fullText": "I am a vendor next door. I heard shouting and saw one man run out without a weapon. He wore a grey tracksuit.",
                            "span": [
                                109,
                                109
                            ]
                        }
                    ]
                },
                {
                    "id": "c_16",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #17",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket and blue jeans while in Statement 2 they were wearing a bright red hoodie with beige cargo pants",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e shop ",
                            "fullText": "I am the shop owner. Two armed men walked in posing as buyers and held my staff at gunpoint. They took diamonds worth eighty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "I was on the street opposite. ",
                            "fullText": "I was on the street opposite. The man I saw fleeing wore a black kurta, not a tracksuit.",
                            "span": [
                                88,
                                88
                            ]
                        }
                    ]
                }
            ],
            "raw_entities": [
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        68,
                        75
                    ],
                    "text": "Tanishq",
                    "label": "PERSON",
                    "attributes": {},
                    "entity_cluster_id": "476de302-8874-4c1a-ad0f-ed212552f7f0"
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        88,
                        95
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "a2099759-8c31-4365-920e-e5cbe0097d88"
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        33,
                        40
                    ],
                    "text": "Tanishq",
                    "label": "PERSON",
                    "attributes": {},
                    "entity_cluster_id": "1b59833b-f6c3-4496-9a2e-5e4af9d2b5f3"
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        22,
                        29
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "2582f533-6fb2-4b53-b15a-296980225c5f"
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        20,
                        27
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "c9c972c2-7204-4821-8e0b-ce57b36c463e"
                }
            ],
            "raw_events": [
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        28,
                        41
                    ],
                    "text": "I was stationed by the glass doors of the Tanishq showroom on MG Road",
                    "subject": "I",
                    "action": "was stationed",
                    "object": "by the glass doors of the Tanishq showroom on MG Road",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        116,
                        130
                    ],
                    "text": "Two masked robbers stormed inside",
                    "subject": "Two masked robbers",
                    "action": "stormed inside",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        152,
                        159
                    ],
                    "text": "The robbers ordered all customers to lie flat on the floor",
                    "subject": "The robbers",
                    "action": "ordered",
                    "object": "all customers to lie flat on the floor",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        7,
                        14
                    ],
                    "text": "The primary robber was wearing a dark leather jacket and blue jeans",
                    "subject": "The primary robber",
                    "action": "was wearing",
                    "object": "a dark leather jacket and blue jeans",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        7,
                        10
                    ],
                    "text": "I run",
                    "subject": "I",
                    "action": "run",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        117,
                        125
                    ],
                    "text": "three robbers sprinted out of the store entrance carrying heavy duffel bags",
                    "subject": "three robbers",
                    "action": "sprinted",
                    "object": "out of the store entrance carrying heavy duffel bags",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        4,
                        14
                    ],
                    "text": "the robbers pushed past frightened pedestrians on the sidewalk as people screamed for police assistance",
                    "subject": "the robbers",
                    "action": "pushed",
                    "object": "past frightened pedestrians on the sidewalk as people screamed for police assistance",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        81,
                        88
                    ],
                    "text": "the commotion erupted",
                    "subject": "the commotion",
                    "action": "erupted",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        0,
                        50
                    ],
                    "text": "the primary robber wore a dark leather jacket",
                    "subject": "the primary robber",
                    "action": "wore",
                    "object": "a dark leather jacket",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        147,
                        151
                    ],
                    "text": "the primary robber fled",
                    "subject": "the primary robber",
                    "action": "fled",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        7,
                        11
                    ],
                    "text": "the primary robber revved a motorcycle",
                    "subject": "the primary robber",
                    "action": "revved",
                    "object": "a motorcycle",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        0,
                        50
                    ],
                    "text": "the primary robber headed",
                    "subject": "the primary robber",
                    "action": "headed",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        2,
                        13
                    ],
                    "text": "I was walking along MG Road",
                    "subject": "I",
                    "action": "was walking",
                    "object": "along MG Road",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        45,
                        51
                    ],
                    "text": "the thieves dashed",
                    "subject": "the thieves",
                    "action": "dashed",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        99,
                        110
                    ],
                    "text": "The primary robber was wearing a bright red hoodie with beige cargo pants",
                    "subject": "The primary robber",
                    "action": "was wearing",
                    "object": "a bright red hoodie with beige cargo pants",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        6,
                        14
                    ],
                    "text": "I securing the cash register",
                    "subject": "I",
                    "action": "securing",
                    "object": "the cash register",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        95,
                        99
                    ],
                    "text": "The thieves took fifty lakhs worth of diamond necklaces and luxury watches from the vault counters",
                    "subject": "The thieves",
                    "action": "took",
                    "object": "fifty lakhs worth of diamond necklaces and luxury watches from the vault counters",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        187,
                        217
                    ],
                    "text": "I emergency sirens began blaring",
                    "subject": "I",
                    "action": "emergency sirens began blaring",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                }
            ]
        },
        "inc-demo05": {
            "statements": [
                {
                    "id": "stmt_0",
                    "witness": "Witness A",
                    "text": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_1",
                    "witness": "Witness B",
                    "text": "I am the customer whose locker was accessed. I had last visited on 10th August. The signatures on the access register do not match mine.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_2",
                    "witness": "Witness C",
                    "text": "I am the bank teller who processed the access request. The individual appeared nervous and left in a hurry after 15 minutes.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_3",
                    "witness": "Witness D",
                    "text": "I am the security guard at the entrance. The individual who entered that day was a woman in a blue saree, not a man.",
                    "status": "Processed"
                },
                {
                    "id": "stmt_4",
                    "witness": "Witness E",
                    "text": "I am the CCTV review officer. The footage from camera 3 clearly shows a woman in blue entering the locker area at 11:42 AM.",
                    "status": "Processed"
                }
            ],
            "markers": [
                {
                    "id": "m_1",
                    "lat": 12.975,
                    "lng": 77.6069,
                    "label": "MG Road",
                    "witness": "Witness A",
                    "color": "blue"
                }
            ],
            "timeline": [
                {
                    "id": "ev_0",
                    "content": "I was stationed by the glass doors of the Tanishq showroom on MG Road",
                    "start": "2024-08-30T14:00:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_1",
                    "content": "Two masked robbers stormed inside",
                    "start": "2024-08-30T14:01:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_2",
                    "content": "The robbers ordered all customers to lie flat on the floor",
                    "start": "2024-08-30T14:02:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_3",
                    "content": "The primary robber was wearing a dark leather jacket and blue jeans",
                    "start": "2024-08-30T14:03:00",
                    "witness": "Witness A",
                    "className": "border-l-4 border-blue-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_4",
                    "content": "I run",
                    "start": "2024-08-30T14:04:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_5",
                    "content": "three robbers sprinted out of the store entrance carrying heavy duffel bags",
                    "start": "2024-08-30T14:05:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_6",
                    "content": "the robbers pushed past frightened pedestrians on the sidewalk as people screamed for p...",
                    "start": "2024-08-30T14:06:00",
                    "witness": "Witness B",
                    "className": "border-l-4 border-red-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_7",
                    "content": "the commotion erupted",
                    "start": "2024-08-30T14:07:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_8",
                    "content": "the primary robber wore a dark leather jacket",
                    "start": "2024-08-30T14:08:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_9",
                    "content": "the primary robber fled",
                    "start": "2024-08-30T14:09:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_10",
                    "content": "the primary robber revved a motorcycle",
                    "start": "2024-08-30T14:10:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_11",
                    "content": "the primary robber headed",
                    "start": "2024-08-30T14:11:00",
                    "witness": "Witness C",
                    "className": "border-l-4 border-green-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_12",
                    "content": "I was walking along MG Road",
                    "start": "2024-08-30T14:12:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_13",
                    "content": "the thieves dashed",
                    "start": "2024-08-30T14:13:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_14",
                    "content": "The primary robber was wearing a bright red hoodie with beige cargo pants",
                    "start": "2024-08-30T14:14:00",
                    "witness": "Witness D",
                    "className": "border-l-4 border-purple-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_15",
                    "content": "I securing the cash register",
                    "start": "2024-08-30T14:15:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_16",
                    "content": "The thieves took fifty lakhs worth of diamond necklaces and luxury watches from the vau...",
                    "start": "2024-08-30T14:16:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                },
                {
                    "id": "ev_17",
                    "content": "I emergency sirens began blaring",
                    "start": "2024-08-30T14:17:00",
                    "witness": "Witness E",
                    "className": "border-l-4 border-yellow-500 bg-[var(--bg-surface)] text-[var(--text-primary)]"
                }
            ],
            "contradictions": [
                {
                    "id": "c_0",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #1",
                    "rationale": "The first statement specifies being stationed by glass doors of a Tanishq showroom, while the second only mentions walking along MG Road without mentioning any specific location or activity.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "dividual pres",
                            "fullText": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                            "span": [
                                28,
                                41
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "am the secu",
                            "fullText": "I am the security guard at the entrance. The individual who entered that day was a woman in a blue saree, not a man.",
                            "span": [
                                2,
                                13
                            ]
                        }
                    ]
                },
                {
                    "id": "c_1",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #2",
                    "rationale": "Statement 1 describes two masked robbers entering a location while Statement 2 mentions three robbers sprinting out carrying duffel bags.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "rty lakhs.",
                            "fullText": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                            "span": [
                                116,
                                126
                            ]
                        },
                        {
                            "witness": "Witness B",
                            "snippet": " do not ",
                            "fullText": "I am the customer whose locker was accessed. I had last visited on 10th August. The signatures on the access register do not match mine.",
                            "span": [
                                117,
                                125
                            ]
                        }
                    ]
                },
                {
                    "id": "c_2",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #3",
                    "rationale": "In Statement 1, it is stated that two masked robbers stormed inside; in contrast, Statement 2 mentions only one robber fleeing.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "rty lakhs.",
                            "fullText": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                            "span": [
                                116,
                                126
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I am the bank teller who proce",
                            "fullText": "I am the bank teller who processed the access request. The individual appeared nervous and left in a hurry after 15 minutes.",
                            "span": [
                                124,
                                124
                            ]
                        }
                    ]
                },
                {
                    "id": "c_3",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #4",
                    "rationale": "The first statement mentions two masked robbers storming in while the second specifies that the primary robber was revving a motorcycle.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "rty lakhs.",
                            "fullText": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                            "span": [
                                116,
                                126
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "e ba",
                            "fullText": "I am the bank teller who processed the access request. The individual appeared nervous and left in a hurry after 15 minutes.",
                            "span": [
                                7,
                                11
                            ]
                        }
                    ]
                },
                {
                    "id": "c_4",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #5",
                    "rationale": "The primary robber in Statement 1 was described as wearing a dark leather jacket and blue jeans, while Statement 2 mentions three robbers sprinting out of the store entrance carrying heavy duffel bags without specifying attire.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e bank ",
                            "fullText": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness B",
                            "snippet": " do not ",
                            "fullText": "I am the customer whose locker was accessed. I had last visited on 10th August. The signatures on the access register do not match mine.",
                            "span": [
                                117,
                                125
                            ]
                        }
                    ]
                },
                {
                    "id": "c_5",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #6",
                    "rationale": "The first statement specifies the attire of the primary robber as a dark leather jacket and blue jeans while the second only mentions that they fled.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e bank ",
                            "fullText": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I am the bank teller who proce",
                            "fullText": "I am the bank teller who processed the access request. The individual appeared nervous and left in a hurry after 15 minutes.",
                            "span": [
                                124,
                                124
                            ]
                        }
                    ]
                },
                {
                    "id": "c_6",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #7",
                    "rationale": "The first statement describes the appearance of the primary robber as wearing a dark leather jacket and blue jeans, while the second statement mentions that they revved a motorcycle.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e bank ",
                            "fullText": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "e ba",
                            "fullText": "I am the bank teller who processed the access request. The individual appeared nervous and left in a hurry after 15 minutes.",
                            "span": [
                                7,
                                11
                            ]
                        }
                    ]
                },
                {
                    "id": "c_7",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #8",
                    "rationale": "The first statement specifies that the primary robber wore a dark leather jacket and blue jeans, while the second statement does not mention any clothing details.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e bank ",
                            "fullText": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I am the bank teller who processed the access requ",
                            "fullText": "I am the bank teller who processed the access request. The individual appeared nervous and left in a hurry after 15 minutes.",
                            "span": [
                                0,
                                50
                            ]
                        }
                    ]
                },
                {
                    "id": "c_8",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #9",
                    "rationale": "The first statement specifies the attire of the primary robber as wearing a dark leather jacket and blue jeans, while the second statement only mentions that the thieves dashed without providing any details about their appearance.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e bank ",
                            "fullText": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "indivi",
                            "fullText": "I am the security guard at the entrance. The individual who entered that day was a woman in a blue saree, not a man.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_9",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #10",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket and blue jeans while in Statement 2 they were wearing a bright red hoodie with beige cargo pants",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e bank ",
                            "fullText": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "saree, not ",
                            "fullText": "I am the security guard at the entrance. The individual who entered that day was a woman in a blue saree, not a man.",
                            "span": [
                                99,
                                110
                            ]
                        }
                    ]
                },
                {
                    "id": "c_10",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #11",
                    "rationale": "Statement 1 describes three robbers sprinting out of a store with heavy duffel bags while Statement 2 mentions only one robber fleeing",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": " do not ",
                            "fullText": "I am the customer whose locker was accessed. I had last visited on 10th August. The signatures on the access register do not match mine.",
                            "span": [
                                117,
                                125
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I am the bank teller who proce",
                            "fullText": "I am the bank teller who processed the access request. The individual appeared nervous and left in a hurry after 15 minutes.",
                            "span": [
                                124,
                                124
                            ]
                        }
                    ]
                },
                {
                    "id": "c_11",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #12",
                    "rationale": "Statement 1 describes robbers sprinting out of a store with heavy duffel bags while Statement 2 only mentions one robber heading somewhere",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": " do not ",
                            "fullText": "I am the customer whose locker was accessed. I had last visited on 10th August. The signatures on the access register do not match mine.",
                            "span": [
                                117,
                                125
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I am the bank teller who processed the access requ",
                            "fullText": "I am the bank teller who processed the access request. The individual appeared nervous and left in a hurry after 15 minutes.",
                            "span": [
                                0,
                                50
                            ]
                        }
                    ]
                },
                {
                    "id": "c_12",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #13",
                    "rationale": "Statement 1 describes robbers sprinting with heavy duffel bags out of a store entrance while Statement 2 states that thieves dashed without specifying their load.",
                    "claims": [
                        {
                            "witness": "Witness B",
                            "snippet": " do not ",
                            "fullText": "I am the customer whose locker was accessed. I had last visited on 10th August. The signatures on the access register do not match mine.",
                            "span": [
                                117,
                                125
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "indivi",
                            "fullText": "I am the security guard at the entrance. The individual who entered that day was a woman in a blue saree, not a man.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_13",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #14",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket while in Statement 2 they were wearing a bright red hoodie with beige cargo pants.",
                    "claims": [
                        {
                            "witness": "Witness C",
                            "snippet": "I am the bank teller who processed the access requ",
                            "fullText": "I am the bank teller who processed the access request. The individual appeared nervous and left in a hurry after 15 minutes.",
                            "span": [
                                0,
                                50
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "saree, not ",
                            "fullText": "I am the security guard at the entrance. The individual who entered that day was a woman in a blue saree, not a man.",
                            "span": [
                                99,
                                110
                            ]
                        }
                    ]
                },
                {
                    "id": "c_14",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #15",
                    "rationale": "The first statement specifies that the primary robber fled, while the second states that all thieves dashed.",
                    "claims": [
                        {
                            "witness": "Witness C",
                            "snippet": "I am the bank teller who proce",
                            "fullText": "I am the bank teller who processed the access request. The individual appeared nervous and left in a hurry after 15 minutes.",
                            "span": [
                                124,
                                124
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "indivi",
                            "fullText": "I am the security guard at the entrance. The individual who entered that day was a woman in a blue saree, not a man.",
                            "span": [
                                45,
                                51
                            ]
                        }
                    ]
                },
                {
                    "id": "c_15",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #16",
                    "rationale": "The first statement specifies that the primary robber wore a dark leather jacket and blue jeans while fleeing in the second.",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e bank ",
                            "fullText": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness C",
                            "snippet": "I am the bank teller who proce",
                            "fullText": "I am the bank teller who processed the access request. The individual appeared nervous and left in a hurry after 15 minutes.",
                            "span": [
                                124,
                                124
                            ]
                        }
                    ]
                },
                {
                    "id": "c_16",
                    "type": "semantic",
                    "title": "Flagged Discrepancy #17",
                    "rationale": "The primary robber in Statement 1 wore a dark leather jacket and blue jeans while in Statement 2 they were wearing a bright red hoodie with beige cargo pants",
                    "claims": [
                        {
                            "witness": "Witness A",
                            "snippet": "e bank ",
                            "fullText": "I am the bank manager. An individual presenting forged KYC documents accessed locker #112 and removed gold worth thirty lakhs.",
                            "span": [
                                7,
                                14
                            ]
                        },
                        {
                            "witness": "Witness D",
                            "snippet": "saree, not ",
                            "fullText": "I am the security guard at the entrance. The individual who entered that day was a woman in a blue saree, not a man.",
                            "span": [
                                99,
                                110
                            ]
                        }
                    ]
                }
            ],
            "raw_entities": [
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        68,
                        75
                    ],
                    "text": "Tanishq",
                    "label": "PERSON",
                    "attributes": {},
                    "entity_cluster_id": "476de302-8874-4c1a-ad0f-ed212552f7f0"
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        88,
                        95
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "a2099759-8c31-4365-920e-e5cbe0097d88"
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        33,
                        40
                    ],
                    "text": "Tanishq",
                    "label": "PERSON",
                    "attributes": {},
                    "entity_cluster_id": "1b59833b-f6c3-4496-9a2e-5e4af9d2b5f3"
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        22,
                        29
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "2582f533-6fb2-4b53-b15a-296980225c5f"
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        20,
                        27
                    ],
                    "text": "MG Road",
                    "label": "LOCATION",
                    "attributes": {},
                    "entity_cluster_id": "c9c972c2-7204-4821-8e0b-ce57b36c463e"
                }
            ],
            "raw_events": [
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        28,
                        41
                    ],
                    "text": "I was stationed by the glass doors of the Tanishq showroom on MG Road",
                    "subject": "I",
                    "action": "was stationed",
                    "object": "by the glass doors of the Tanishq showroom on MG Road",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        116,
                        130
                    ],
                    "text": "Two masked robbers stormed inside",
                    "subject": "Two masked robbers",
                    "action": "stormed inside",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        152,
                        159
                    ],
                    "text": "The robbers ordered all customers to lie flat on the floor",
                    "subject": "The robbers",
                    "action": "ordered",
                    "object": "all customers to lie flat on the floor",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_0",
                    "source_span": [
                        7,
                        14
                    ],
                    "text": "The primary robber was wearing a dark leather jacket and blue jeans",
                    "subject": "The primary robber",
                    "action": "was wearing",
                    "object": "a dark leather jacket and blue jeans",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        7,
                        10
                    ],
                    "text": "I run",
                    "subject": "I",
                    "action": "run",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        117,
                        125
                    ],
                    "text": "three robbers sprinted out of the store entrance carrying heavy duffel bags",
                    "subject": "three robbers",
                    "action": "sprinted",
                    "object": "out of the store entrance carrying heavy duffel bags",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_1",
                    "source_span": [
                        4,
                        14
                    ],
                    "text": "the robbers pushed past frightened pedestrians on the sidewalk as people screamed for police assistance",
                    "subject": "the robbers",
                    "action": "pushed",
                    "object": "past frightened pedestrians on the sidewalk as people screamed for police assistance",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        81,
                        88
                    ],
                    "text": "the commotion erupted",
                    "subject": "the commotion",
                    "action": "erupted",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        0,
                        50
                    ],
                    "text": "the primary robber wore a dark leather jacket",
                    "subject": "the primary robber",
                    "action": "wore",
                    "object": "a dark leather jacket",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        147,
                        151
                    ],
                    "text": "the primary robber fled",
                    "subject": "the primary robber",
                    "action": "fled",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        7,
                        11
                    ],
                    "text": "the primary robber revved a motorcycle",
                    "subject": "the primary robber",
                    "action": "revved",
                    "object": "a motorcycle",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_2",
                    "source_span": [
                        0,
                        50
                    ],
                    "text": "the primary robber headed",
                    "subject": "the primary robber",
                    "action": "headed",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        2,
                        13
                    ],
                    "text": "I was walking along MG Road",
                    "subject": "I",
                    "action": "was walking",
                    "object": "along MG Road",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        45,
                        51
                    ],
                    "text": "the thieves dashed",
                    "subject": "the thieves",
                    "action": "dashed",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_3",
                    "source_span": [
                        99,
                        110
                    ],
                    "text": "The primary robber was wearing a bright red hoodie with beige cargo pants",
                    "subject": "The primary robber",
                    "action": "was wearing",
                    "object": "a bright red hoodie with beige cargo pants",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        6,
                        14
                    ],
                    "text": "I securing the cash register",
                    "subject": "I",
                    "action": "securing",
                    "object": "the cash register",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        95,
                        99
                    ],
                    "text": "The thieves took fifty lakhs worth of diamond necklaces and luxury watches from the vault counters",
                    "subject": "The thieves",
                    "action": "took",
                    "object": "fifty lakhs worth of diamond necklaces and luxury watches from the vault counters",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                },
                {
                    "source_statement_id": "stmt_4",
                    "source_span": [
                        187,
                        217
                    ],
                    "text": "I emergency sirens began blaring",
                    "subject": "I",
                    "action": "emergency sirens began blaring",
                    "object": "",
                    "time_ref": None,
                    "location_ref": None,
                    "confidence": 1.0,
                    "low_confidence": False,
                    "negated": False
                }
            ]
        }
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# PERSISTENT STORAGE  (SQLite — survives server restarts)
# ─────────────────────────────────────────────────────────────────────────────
import sqlite3
import json as _json
import os as _os

_DB_PATH = _os.path.join(_os.path.dirname(__file__), "silent_witness.db")

def _get_db():
    """Return a thread-local SQLite connection with WAL mode for concurrency."""
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn

def _init_db():
    """Create tables if they don't exist and seed demo incidents."""
    conn = _get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id TEXT PRIMARY KEY,
            title TEXT,
            type TEXT,
            date TEXT,
            status TEXT,
            witness_count INTEGER,
            contradiction_count INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS incident_data (
            incident_id TEXT PRIMARY KEY,
            data_json TEXT,
            FOREIGN KEY(incident_id) REFERENCES incidents(id)
        )
    """)
    conn.commit()

    # Seed demo incidents from the in-memory DB only if the table is empty
    cur = conn.execute("SELECT COUNT(*) FROM incidents")
    if cur.fetchone()[0] == 0:
        for inc in DB["incidents"]:
            conn.execute(
                "INSERT OR IGNORE INTO incidents VALUES (?,?,?,?,?,?,?)",
                (inc["id"], inc["title"], inc["type"], inc["date"],
                 inc["status"], inc["witnessCount"], inc["contradictionCount"])
            )
        for inc_id, inc_data in DB["incident_data"].items():
            conn.execute(
                "INSERT OR IGNORE INTO incident_data VALUES (?,?)",
                (inc_id, _json.dumps(inc_data))
            )
        conn.commit()
    conn.close()

_init_db()  # run once at startup

def _db_get_incidents():
    conn = _get_db()
    rows = conn.execute("SELECT * FROM incidents ORDER BY rowid DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def _db_get_incident_data(incident_id: str):
    conn = _get_db()
    row = conn.execute(
        "SELECT data_json FROM incident_data WHERE incident_id=?", (incident_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    return _json.loads(row["data_json"])

def _db_save_incident(summary: dict, data: dict):
    conn = _get_db()
    conn.execute(
        "INSERT OR REPLACE INTO incidents VALUES (?,?,?,?,?,?,?)",
        (summary["id"], summary["title"], summary["type"], summary["date"],
         summary["status"], summary["witnessCount"], summary["contradictionCount"])
    )
    conn.execute(
        "INSERT OR REPLACE INTO incident_data VALUES (?,?)",
        (summary["id"], _json.dumps(data))
    )
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Convert ML pipeline output → UI-ready incident data
# ─────────────────────────────────────────────────────────────────────────────

# Known Indian city coordinates for spatial resolution
_KNOWN_COORDS = {
    "mg road":          (12.9757, 77.6011),
    "mg road bengaluru":(12.9757, 77.6011),
    "commercial street":(12.9814, 77.6097),
    "indiranagar":      (12.9783, 77.6408),
    "chickpet":         (12.9641, 77.5759),
    "koramangala":      (12.9279, 77.6271),
    "connaught place":  (28.6315, 77.2167),
    "chandni chowk":    (28.6562, 77.2310),
    "marine drive":     (18.9440, 72.8237),
    "railway station":  (28.6420, 77.2197),
    "police station":   (28.6429, 77.2195),
}

def _resolve_coordinates(location_text: str):
    """Try to resolve a location name to (lat, lng). Returns None if unknown."""
    t = location_text.lower().strip()
    for key, coords in _KNOWN_COORDS.items():
        if key in t:
            return coords
    return None

def _ml_results_to_ui(req_statements: List[str], title: str, results: dict) -> tuple:
    """
    Convert ML pipeline results → (summary_dict, incident_data_dict).
    Wires temporals → timeline and spatials → map markers from real ML output.
    Character spans are always clamped to the actual submitted statement lengths
    so highlighting never overruns the text (fixes the fallback span-mapping bug).
    """
    import datetime as _dt

    inc_id = f"inc-{uuid.uuid4().hex[:6]}"
    colors = ["border-blue-500", "border-red-500", "border-green-500",
              "border-purple-500", "border-yellow-500"]

    # --- Statements ---
    ui_statements = [
        {"id": f"stmt_{i}", "witness": f"Witness {chr(65+i)}", "text": text, "status": "Processed"}
        for i, text in enumerate(req_statements)
    ]

    # --- Contradictions (clamp spans to actual text length) ---
    ui_contradictions = []
    for i, d in enumerate(results.get("contradictions", [])):
        claims = []
        for span_info in d.get("source_span", []):
            stmt_id  = span_info[0]
            span_range = span_info[1]
            stmt_idx = int(stmt_id.split('_')[-1]) if '_' in stmt_id else 0
            full_text = req_statements[stmt_idx] if stmt_idx < len(req_statements) else ""
            text_len  = len(full_text)
            # Clamp span to actual submitted text — this is the fix for Issue 5
            if len(span_range) == 2:
                start = max(0, min(int(span_range[0]), text_len))
                end   = max(start, min(int(span_range[1]), text_len))
            else:
                start, end = 0, 0
            snippet = full_text[start:end] if end > start else (full_text[:60] + "…" if full_text else "—")
            claims.append({
                "witness":  f"Witness {chr(65+stmt_idx)}",
                "snippet":  snippet,
                "fullText": full_text,
                "span":     [start, end]
            })
        ui_contradictions.append({
            "id":       f"c_{i}",
            "type":     d.get("type", "semantic"),
            "title":    f"Flagged Discrepancy #{i+1}",
            "rationale":d.get("rationale", "Statements conflict."),
            "claims":   claims
        })

    # --- Timeline: prefer real temporals from ML, fall back to event sequence ---
    ui_timeline = []
    temporals = results.get("temporals", [])
    if temporals:
        for i, t in enumerate(temporals):
            stmt_idx = int(t.get("source_statement_id", "stmt_0").split('_')[-1])
            resolved = t.get("resolved_time") or t.get("text", "")
            try:
                ts = _dt.datetime.fromisoformat(resolved)
            except Exception:
                ts = _dt.datetime.now() - _dt.timedelta(minutes=30 - i)
            ui_timeline.append({
                "id":        f"ev_{i}",
                "content":   t.get("text", "Temporal reference"),
                "start":     ts.isoformat(),
                "witness":   f"Witness {chr(65 + stmt_idx)}",
                "className": f"border-l-4 {colors[stmt_idx % len(colors)]} bg-[var(--bg-surface)] text-[var(--text-primary)]"
            })
    else:
        # Fallback: use event tuples with dummy sequential timestamps
        for i, ev in enumerate(results.get("events", [])):
            stmt_idx = int(ev.get("source_statement_id", "stmt_0").split('_')[-1])
            ts = _dt.datetime.now() - _dt.timedelta(minutes=30 - i)
            content = f"{ev.get('subject', '')} {ev.get('action', 'event')} {ev.get('object', '')}".strip()
            ui_timeline.append({
                "id":        f"ev_{i}",
                "content":   content or "Unnamed event",
                "start":     ts.isoformat(),
                "witness":   f"Witness {chr(65 + stmt_idx)}",
                "className": f"border-l-4 {colors[stmt_idx % len(colors)]} bg-[var(--bg-surface)] text-[var(--text-primary)]"
            })

    # --- Map markers: prefer real spatials from ML, fall back to location entities ---
    ui_markers = []
    spatials = results.get("spatials", [])
    placed: set = set()
    if spatials:
        for i, s in enumerate(spatials):
            stmt_idx = int(s.get("source_statement_id", "stmt_0").split('_')[-1])
            loc_text = s.get("text", "")
            coords   = _resolve_coordinates(loc_text)
            if coords is None:
                # Spread unknown locations near a neutral base point with small offset
                coords = (28.6139 + i * 0.001, 77.2090 + i * 0.001)
            key = f"{coords[0]:.4f},{coords[1]:.4f}"
            if key in placed:
                continue  # deduplicate same location
            placed.add(key)
            ui_markers.append({
                "id":      f"m_{i}",
                "lat":     coords[0],
                "lng":     coords[1],
                "label":   loc_text,
                "witness": f"Witness {chr(65 + stmt_idx)}",
                "color":   "blue"
            })
    else:
        # Fallback: use LOCATION entities
        for i, ent in enumerate(results.get("entities", [])):
            if ent.get("label") in ["LOCATION", "FACILITY", "FAC"]:
                stmt_idx = int(ent.get("source_statement_id", "stmt_0").split('_')[-1])
                loc_text = ent.get("text", "")
                coords   = _resolve_coordinates(loc_text)
                if coords is None:
                    coords = (28.6139 + i * 0.001, 77.2090 + i * 0.001)
                key = f"{coords[0]:.4f},{coords[1]:.4f}"
                if key in placed:
                    continue
                placed.add(key)
                ui_markers.append({
                    "id":      f"m_{i}",
                    "lat":     coords[0],
                    "lng":     coords[1],
                    "label":   loc_text,
                    "witness": f"Witness {chr(65 + stmt_idx)}",
                    "color":   "blue"
                })

    summary = {
        "id":                inc_id,
        "title":             title,
        "type":              "Investigation",
        "date":              _dt.date.today().isoformat(),
        "status":            "Reviewing",
        "witnessCount":      len(req_statements),
        "contradictionCount":len(ui_contradictions)
    }
    data = {
        "statements":    ui_statements,
        "markers":       ui_markers,
        "timeline":      ui_timeline,
        "contradictions":ui_contradictions,
        "raw_entities":  results.get("entities", []),
        "raw_events":    results.get("events", []),
        "raw_temporals": results.get("temporals", []),
        "raw_spatials":  results.get("spatials", []),
    }
    return inc_id, summary, data

# ─────────────────────────────────────────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────────────────────────────────────────
class IncidentRequest(BaseModel):
    statements: List[str]
    title: str = "New Incident"

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Silent Witness Backend is running"}

@app.get("/api/incidents")
def get_incidents():
    rows = _db_get_incidents()
    # Normalize column names for frontend (snake_case → camelCase)
    return [
        {
            "id":                r.get("id"),
            "title":             r.get("title"),
            "type":              r.get("type"),
            "date":              r.get("date"),
            "status":            r.get("status"),
            "witnessCount":      r.get("witness_count", r.get("witnessCount", 0)),
            "contradictionCount":r.get("contradiction_count", r.get("contradictionCount", 0)),
        }
        for r in rows
    ]

@app.get("/api/incidents/{incident_id}")
def get_incident_data(incident_id: str):
    data = _db_get_incident_data(incident_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return data

@app.post("/analyze")
def analyze_statements(req: IncidentRequest):
    if not req.statements:
        raise HTTPException(status_code=400, detail="Must provide at least one statement.")
    try:
        from ml_core.orchestrator import analyze_incident
        return analyze_incident(req.statements)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/incidents")
def create_incident(req: IncidentRequest):
    """
    Run ML pipeline on submitted testimonies and persist the result.
    
    Fallback behaviour (when LM Studio is offline):
    - Loads theft_case_output.json for ML results (contradictions, events, etc.)
    - BUT keeps the user's ORIGINAL submitted statements as the statement text.
    - Clamps all character spans from the fallback JSON to fit within the user's text.
    This ensures the Discrepancy Inspector never highlights garbage indices.
    """
    if not req.statements:
        raise HTTPException(status_code=400, detail="Must provide at least one statement.")

    try:
        using_fallback = False
        try:
            from ml_core.orchestrator import analyze_incident
            results = analyze_incident(req.statements)
            if not results or "contradictions" not in results:
                raise ValueError("Invalid ML pipeline output structure")
        except Exception as e:
            import logging
            logging.warning(f"ML Pipeline unavailable ({e}). Using theft_case_output.json fallback...")
            using_fallback = True
            fallback_path = _os.path.join(_os.path.dirname(__file__), "theft_case_output.json")
            if _os.path.exists(fallback_path):
                with open(fallback_path, "r", encoding="utf-8") as f:
                    results = _json.load(f)
            else:
                raise HTTPException(
                    status_code=503,
                    detail=f"ML pipeline unavailable ({str(e)}) and no fallback file found."
                )

        inc_id, summary, data = _ml_results_to_ui(req.statements, req.title, results)

        if using_fallback:
            # Mark in the summary so the UI can show a banner
            summary["status"] = "Demo (Fallback)"

        _db_save_incident(summary, data)
        return {"id": inc_id, "summary": summary}
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

class FeedbackRequest(BaseModel):
    detection_result_id: str
    reviewer_verdict: str = "confirmed"
    note: Optional[str] = ""

@app.post("/api/feedback")
def submit_feedback(req: FeedbackRequest):
    try:
        from ml_core.feedback import record_feedback
        entry = record_feedback(req.detection_result_id, req.reviewer_verdict, req.note or "")
        return {"status": "success", "feedback": entry}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)

