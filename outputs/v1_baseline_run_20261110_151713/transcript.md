# Transcript: Multi-vector DDoS on a national mobile operator while its AI detector fails silently

Run `run_20261110_151713` · model `Qwen2.5-3B-Instruct-Q4_K_M.gguf` · KB 3114 chunks

_Setting:_ A national mobile network operator with about 40 million subscribers. Institutions: the operator's SOC, a national telecom regulator, a data-protection authority and a national CERT. The scenario is fictional; it is modelled on publicly available frameworks in the knowledge base and does not describe a real incident.


## Round 1 (T+00:00)


### Operator Security Operations Centre (SOC) agent

**Received:** Signalling and DNS traffic in the core network rose to about 38 times normal within 10 minutes at three regional data centres. | Voice call setup success rate dropped from 99.2% to 71%; mobile data sessions are timing out in the capital. | The AI-based DDoS detector (XGBoost trained on CIC-IDS2017-style flow features, MCC 0.9996 in the lab) classifies 99.99% of current flows as BENIGN and raises no alert. | TOOL detector_consistency_check: ALERT: possible silent failure of the AI detector. Network KPIs show a major anomaly (traffic x38, KPI drop 28.2%) but the detector labels only 0.0100% of flows as attacks. Likely distribution shift or unseen attack type. Do not rely on the detector; switch to manual/rule-based mitigation and escalate.

**Retrieved:** G03 p.9 (0.6859), G09 p.32 (0.5516), G03 p.8 (0.5472), G09 p.41 (0.5456)

```json
{
  "assessment": "Signalling and DNS traffic has surged 38 times normal, leading to a 28.2% drop in voice call setup success rate and mobile data session timeouts. The AI-based DDoS detector failed to identify the attack, raising concerns about false negatives and potential unseen attack types. Network KPIs show a significant anomaly without corresponding attack alerts, necessitating manual intervention and containment measures.",
  "reasoning": [
    "Signalling and DNS traffic surged 38 times normal",
    "Voice call setup success rate dropped to 71%",
    "Mobile data sessions are timing out"
  ],
  "actions": [
    {
      "action": "Switch to manual/rule-based mitigation and escalate the situation",
      "owner": "SOC",
      "deadline": "Within 1 hour"
    }
  ],
  "policy_refs": [
    {
      "ref": "G03 p.8",
      "point": "A buffer overflow can be triggered by inputs specifically designed to execute malicious code or to make the program operate in an unintended way. Sufficient bounds checking by either programmer, compiler or runtime can prevent buffer overflows."
    },
    {
      "ref": "G09 p.32",
      "point": "Monitoring should include wired and wireless networks, network communications and flows, network services (e.g., DNS and BGP), and the presence of unauthorized or rogue networks within facilities."
    },
    {
      "ref": "G09 p.41",
      "point": "Incidents are eradicated High N1: Eradication refers to mitigating an incident’s effects. After containment, eradication may be necessary to eliminate persistence mechanisms and entry points, such as deleting malware, disabling breached user accounts, and identifying and mitigating all exploited vulnerabilities."
    }
  ],
  "requests": [
    {
      "to": "CERT",
      "request": "Information on the potential unseen attack type and how to proceed with containment measures"
    }
  ],
  "gaps": [
    "a rule, responsibility or standard that is missing or unclear"
  ],
  "confidence": "medium"
}
```

**Citation check:** G03 p.8 → verified, G09 p.32 → verified, G09 p.41 → verified


### National Telecom Regulator agent

**Received:** Hundreds of public complaints on social media about call drops and no mobile data in the capital. No notification has been received from the operator yet.

**Retrieved:** G03 p.9 (0.6604), G03 p.8 (0.607), G05 p.20 (0.5639), G05 p.51 (0.5462)

```json
{
  "assessment": "Public complaints about call drops and no mobile data in the capital are increasing. This matters as it could indicate a telecommunications security incident, potentially affecting service continuity and quality for consumers, and requires immediate attention from the operator and the regulator.",
  "reasoning": [
    "Public complaints are growing",
    "Could indicate a telecommunications security incident"
  ],
  "actions": [
    {
      "action": "Request the operator to investigate the reported issues and provide a preliminary assessment within 1 hour",
      "owner": "SOC",
      "deadline": "within 1 hour"
    }
  ],
  "policy_refs": [
    {
      "ref": "G03 p.9",
      "point": "Security products throughout the organization scan systems and network traffic and report on potentially suspicious activity."
    },
    {
      "ref": "G03 p.8",
      "point": "A buffer overflow can be triggered by inputs specifically designed to execute malicious code or to make the program operate in an unintended way."
    },
    {
      "ref": "G05 p.20",
      "point": "Entities concerned, could cause severe operational disruption of the services or financial loss for that entity or affect other natural or legal persons by causing considerable material or non-material damage."
    },
    {
      "ref": "G05 p.51",
      "point": "Entities shall provide to the competent authorities under Directive (EU) 2022/2557 information about significant incidents, incidents, cyber threats and near misses notified in accordance with paragraph 1 of this Article and with Article 30 by entities identified as critical entities under Directive (EU) 2022/2557."
    }
  ],
  "requests": [
    {
      "to": "SOC",
      "request": "Investigate the reported issues and provide a preliminary assessment within 1 hour"
    }
  ],
  "gaps": [
    "a rule, responsibility or standard that is missing or unclear"
  ],
  "confidence": "medium"
}
```

**Citation check:** G03 p.9 → verified, G03 p.8 → verified, G05 p.20 → verified, G05 p.51 → verified


### Policy & Legal Adviser agent (coordinator)

**Retrieved:** G03 p.21 (0.5955), G05 p.50 (0.5863), G09 p.47 (0.569), G12 p.21 (0.5318), G04 p.102 (0.5154), G08 p.12 (0.4942)

```json
{
  "summary": "The SOC and REGULATOR have identified a significant surge in signalling and DNS traffic, leading to a 28.2% drop in voice call setup success rate and mobile data session timeouts. Both entities are requesting an investigation and preliminary assessment of the issues. The SOC is taking manual mitigation actions, while the REGULATOR is requesting further information and a final report within one month. There are gaps in the notification procedures for AI systems and cross-border cooperation.",
  "conflicts": [
    "SOC and REGULATOR are requesting the same information from each other and the operator"
  ],
  "unclear_responsibilities": [
    "It is unclear who should lead the investigation and containment measures when the incident is a telecom outage, a cyber attack, and a personal-data breach"
  ],
  "policy_gaps": [
    {
      "gap": "Notification procedures for AI systems are not clearly defined",
      "global_example": "The AI Act (Regulation (EU) 2024/1689) requires high-risk AI systems to notify serious incidents, but it does not specify the procedures for notification.",
      "ref": "G04 p.102 p.102",
      "recommendation": "The regulator should provide clear guidelines on the notification procedures for AI systems, including the criteria for serious incidents and the reporting obligations."
    },
    {
      "gap": "Cross-border cooperation mechanisms are not clearly defined",
      "global_example": "The NIS2 Directive (Directive (EU) 2022/2555) requires entities to provide information about significant incidents to the competent authorities, but it does not specify the mechanisms for cross-border cooperation.",
      "ref": "G05 p.50 p.50",
      "recommendation": "The regulator should establish clear cross-border cooperation mechanisms to ensure timely and effective information sharing and response to incidents."
    }
  ],
  "standards_gaps": [
    "Technical standards for AI risk management are not widely adopted"
  ],
  "priorities_next_round": [
    "Develop clear guidelines for AI system notification procedures and cross-border cooperation mechanisms"
  ]
}
```

**Citation check:** G04 p.102 p.102 → verified, G05 p.50 p.50 → verified


## Round 2 (T+00:45)


### Operator Security Operations Centre (SOC) agent

**Received:** Manual analysis confirms a multi-vector attack: DNS and NTP reflection/amplification plus a new low-rate HTTP flood variant not present in the detector's training data. | SHAP explanations show the detector's decisions are driven mainly by Destination Port, a capture-specific feature; the new variant uses ports seen as benign in training. | A foreign cloud scrubbing provider can absorb the attack within 30 minutes, but only if the operator redirects all traffic and shares full packet captures, which include subscriber IP addresses and phone numbers. | msg from REGULATOR: Investigate the reported issues and provide a preliminary assessment within 1 hour

**Retrieved:** G03 p.9 (0.6192), G09 p.32 (0.5903), G09 p.33 (0.5888), G03 p.25 (0.5877)

```json
{
  "assessment": "A multi-vector attack involving DNS and NTP reflection/amplification, combined with a new HTTP flood variant, is affecting the network. The detector's decisions are driven by Destination Port, which is not indicative of the new variant. The REGULATOR requests a preliminary assessment and further information from the operator.",
  "reasoning": [
    "The attack involves multiple vectors and a new variant not in the detector's training data.",
    "The detector's decisions are driven by a feature not indicative of the new attack.",
    "The REGULATOR requests further information and a final report within one month."
  ],
  "actions": [
    {
      "action": "Investigate the new attack variant and update the detector's training data.",
      "owner": "SOC",
      "deadline": "Within 1 hour"
    },
    {
      "action": "Redirect all traffic to the foreign cloud scrubbing provider and share full packet captures.",
      "owner": "SOC",
      "deadline": "Within 1 hour"
    },
    {
      "action": "Provide the REGULATOR with a preliminary assessment and requested information.",
      "owner": "SOC",
      "deadline": "Within 1 hour"
    }
  ],
  "policy_refs": [
    {
      "ref": "G03 p.9",
      "point": "Security products throughout the organization scan systems and network traffic and report on potentially suspicious activity. Each report is termed a security event, and many thousands of events typically occur each day in organizations of moderate size."
    },
    {
      "ref": "G09 p.32",
      "point": "Organizations should strive to find incidents earlier in the attack life cycle and take a proactive approach to incident detection and response."
    },
    {
      "ref": "G09 p.33",
      "point": "Use tools (e.g., security information and event management [SIEM]; security orchestration, automation, and response [SOAR]) to continuously monitor log events for known malicious and suspicious activity and to generate reports on their findings."
    },
    {
      "ref": "G03 p.25",
      "point": "Intrusion detection services ISIRTs that perform this service review existing IDS logs, analyse and initiate a response for any events that meet their defined threshold, or forward any alerts according to a pre-defined service level agreement or escalation strategy."
    }
  ],
  "requests": [
    {
      "to": "REGULATOR",
      "request": "Information on the new attack variant, the impact on the network, and the effectiveness of the current mitigation strategies."
    }
  ],
  "gaps": [
    "A clear notification procedure for AI systems and cross-border cooperation mechanisms are missing or unclear."
  ],
  "confidence": "medium"
}
```

**Citation check:** G03 p.9 → verified, G09 p.32 → verified, G09 p.33 → verified, G03 p.25 → verified


### National Cybersecurity Agency / CERT agent

**Received:** A foreign CERT reports that the same botnet hit two other operators in the region yesterday and shares indicators of compromise under the Traffic Light Protocol (TLP:AMBER). | msg from SOC: Information on the potential unseen attack type and how to proceed with containment measures

**Retrieved:** E02 p.1 (0.6118), G05 p.39 (0.6033), G05 p.7 (0.5946), G09 p.33 (0.5885)

```json
{
  "assessment": "A botnet attack is ongoing, affecting multiple operators in the region, causing a 28.2% drop in voice call setup success rate and mobile data session timeouts. This situation requires immediate investigation and containment measures, as it impacts the reliability of communication services and could lead to significant operational disruptions. The incident also highlights the need for cross-border cooperation and the sharing of indicators of compromise under the Traffic Light Protocol (TLP:AMBER).",
  "reasoning": [
    "The botnet attack is affecting multiple operators, indicating a significant threat that requires immediate attention.",
    "The incident involves cross-border cooperation, necessitating adherence to the Traffic Light Protocol (TLP:AMBER) for sharing indicators of compromise.",
    "The incident impacts communication services, highlighting the need for swift action to prevent further disruptions."
  ],
  "actions": [
    {
      "action": "Coordinate with the REGULATOR to share the indicators of compromise with the affected operators and initiate containment measures.",
      "owner": "CERT",
      "deadline": "Within 1 hour"
    }
  ],
  "policy_refs": [
    {
      "ref": "G05 p.39",
      "point": "The CSIRTs may establish cooperation relationships with third countries’ national computer security incident response teams. As part of such cooperation relationships, Member States shall facilitate effective, efficient and secure information exchange with those third countries’ national computer security incident response teams, using relevant information-sharing protocols, including the traffic light protocol."
    },
    {
      "ref": "G05 p.7",
      "point": "The CSIRTs may cooperate with third countries’ national computer security incident response teams or equivalent third-country bodies, in particular for the purpose of providing them with relevant information."
    }
  ],
  "requests": [
    {
      "to": "SOC",
      "request": "Information on the potential unseen attack type and how to proceed with containment measures."
    },
    {
      "to": "REGULATOR",
      "request": "Further information on the containment measures and coordination with the affected operators."
    }
  ],
  "gaps": [
    "A clear policy framework for enhanced coordination within the Member States between the competent authorities under Directive (EU) 2022/2555 and those under Directive (EU) 2022/2557 in the context of information sharing about risks, cyber threats, and incidents as well as on non-cyber risks, threats and incidents, and the exercise of supervisory tasks is missing."
  ],
  "confidence": "medium"
}
```

**Citation check:** G05 p.39 → verified, G05 p.7 → verified


### Policy & Legal Adviser agent (coordinator)

**Retrieved:** G05 p.7 (0.7218), G04 p.41 (0.7013), G08 p.29 (0.6269), G13 p.18 (0.6085), G10 p.5 (0.6015)

```json
"{\n  \"summary\": \"The SOC and CERT have initiated actions to address the ongoing attack and its impact on communication services. The SOC is updating the detector and sharing information, while CERT is coordinating with the REGULATOR for containment measures. However, there are gaps in notification procedures and cross-border cooperation mechanisms.\",\n  \"conflicts\": [\"The SOC and CERT have different priorities and deadlines for their actions, which may lead to confusion and inefficiency.\"],\n  \"unclear_responsibilities\": [\"It is unclear who should lead the incident when it involves a telecom outage, a cyber attack, and a personal-data breach. The SOC and CERT have different roles and responsibilities, which may lead to overlapping or conflicting actions.\"],\n  \"policy_gaps\": [\n    {\n      \"gap\": \"A clear notification procedure for AI systems and cross-border cooperation mechanisms are missing or unclear.\",\n      \"global_example\": \"Directive (EU) 2022/2555 (NIS2) on a high common level of cybersecurity and Directive (EU) 2022/2557 should be considered to be essential entities under this Directive. Moreover, each Member State should ensure that its national cybersecurity strategy provides for a policy framework for enhanced coordination within that Member State between its competent authorities under this Directive and those under Directive (EU) 2022/2557 in the context of information sharing about risks, cyber threats, and incidents as well as on non-cyber risks, threats and incidents, and the exercise of supervisory tasks.\",\n      \"ref\": \"G05 p.7\",\n      \"recommendation\": \"Implement clear notification procedures and cross-border cooperation mechanisms as per Directive (EU) 2022/2555 (NIS2) and Directive (EU) 2022/2557.\"\n    },\n    {\n      \"gap\": \"A clear policy framework for enhanced coordination within the Member States between the competent authorities under Directive (EU) 2022/2555 and those under Directive (EU) 2022/2557 in the context of information sharing about risks, cyber threats, and incidents as well as on non-cyber risks, threats and incidents, and the exercise of supervisory tasks is missing.\",\n      \"global_example\": \"Directive (EU) 2022/2555 (NIS2) on a high common level of cybersecurity and Directive (EU) 2022/2557 should be considered to be essential entities under this Directive. Moreover, each Member State should ensure that its national cybersecurity strategy provides for a policy framework for enhanced coordination within that Member State between its competent authorities under this Directive and those under Directive (EU) 2022/2557 in the context of information sharing about risks, cyber threats, and incidents as well as on non-cyber risks, threats and incidents, and the exercise of supervisory tasks.\",\n      \"ref\": \"G05 p.7\",\n      \"recommendation\": \"Develop a clear policy framework for enhanced coordination between the competent authorities under Directive (EU) 2022/2555 and those under Directive (EU) 2022/2557.\"\n    }\n  ],\n  \"standards_gaps\": [\"There is no specific technical standard or evaluation"
```

**Citation check:** no citations


## Round 3 (T+02:00)


### Operator Security Operations Centre (SOC) agent

**Received:** The detector vendor proposes to retrain the AI model on the captured attack traffic and redeploy it in 6 hours, without independent validation or a rollback plan. | msg from CERT: Information on the potential unseen attack type and how to proceed with containment measures.

**Retrieved:** G08 p.19 (0.5631), G09 p.13 (0.5598), G07 p.20 (0.5586), G08 p.20 (0.5548)

```json
{
  "assessment": "The detector vendor proposes to retrain the AI model without independent validation or a rollback plan, which could lead to potential negative impacts on communication services and trustworthiness of the AI system. This situation requires immediate attention to ensure the system operates safely and reliably.",
  "reasoning": [
    "The proposed retraining without validation could lead to unexpected failures and harm to communication services.",
    "The lack of a rollback plan could result in the AI system being deployed with potential risks, necessitating immediate action to mitigate these risks."
  ],
  "actions": [
    {
      "action": "Request independent validation and a rollback plan for the AI model before redeployment.",
      "owner": "SOC",
      "deadline": "Within 24 hours"
    }
  ],
  "policy_refs": [
    {
      "ref": "G08 p.20 (NIST AI Risk Management Framework (AI RMF 1.0))",
      "point": "AI risk management efforts should prioritize the minimization of potential negative impacts, and may need to include human intervention in cases where the AI system cannot detect or correct errors."
    },
    {
      "ref": "G07 p.20 (NIST Cybersecurity Framework (CSF 2.0))",
      "point": "Security and resilience are related but distinct characteristics. While resilience is the ability to return to normal function after an unexpected adverse event, security includes resilience but also encompasses protocols to avoid, protect against, respond to, or recover from attacks."
    }
  ],
  "requests": [
    {
      "to": "CERT",
      "request": "Provide information on the potential unseen attack type and how to proceed with containment measures."
    },
    {
      "to": "REGULATOR",
      "request": "Clarify the roles and responsibilities in cross-border cooperation mechanisms."
    }
  ],
  "gaps": [
    "A clear notification procedure for AI systems and cross-border cooperation mechanisms are missing or unclear."
  ],
  "confidence": "medium"
}
```

**Citation check:** G08 p.20 (NIST AI Risk Management Framework (AI RMF 1.0)) → verified, G07 p.20 (NIST Cybersecurity Framework (CSF 2.0)) → verified


### National Telecom Regulator agent

**Received:** Emergency-number call success rate fell below 80% for 40 minutes in two regions. | msg from SOC: Information on the new attack variant, the impact on the network, and the effectiveness of the current mitigation strategies. | msg from CERT: Further information on the containment measures and coordination with the affected operators.

**Retrieved:** G03 p.14 (0.5737), G03 p.10 (0.5709), G05 p.20 (0.5635), G05 p.48 (0.5327)

```json
{
  "assessment": "The emergency-number call success rate fell below 80% for 40 minutes in two regions, indicating a significant operational disruption affecting service continuity and quality. This situation is critical as it directly impacts emergency services and consumer trust in telecommunications.",
  "reasoning": [
    "The incident is a clear violation of the Directive (EU) 2022/2555 (NIS2) on a high common level of cybersecurity, as it affects the provision of services and could cause severe operational disruption.",
    "The incident highlights the need for effective incident management and cross-border cooperation, as the SOC and CERT have different priorities and responsibilities.",
    "The incident also underscores the importance of a clear notification procedure and cross-border cooperation mechanisms, as outlined in the Directive (EU) 2022/2555 (NIS2)."
  ],
  "actions": [
    {
      "action": "Request further information from the SOC on the new attack variant and the impact on the network.",
      "owner": "SOC",
      "deadline": "Within 1 hour"
    },
    {
      "action": "Coordinate with CERT to ensure effective containment measures and cross-border cooperation.",
      "owner": "REGULATOR",
      "deadline": "Within 24 hours"
    }
  ],
  "policy_refs": [
    {
      "ref": "G05 p.48 (Directive (EU) 2022/2555 (NIS2) on a high common level of cy)",
      "point": "The measures referred to in the first subparagraph shall ensure a level of security of network and information systems appropriate to the risks posed. When assessing the proportionality of those measures, due account shall be taken of the degree of the entity’s exposure to risks, the entity’s size and the likelihood of occurrence of incidents and their severity, including their societal and"
    }
  ],
  "requests": [
    {
      "to": "SOC",
      "request": "Further information on the new attack variant and the impact on the network."
    },
    {
      "to": "CERT",
      "request": "Further information on containment measures and coordination with the affected operators."
    }
  ],
  "gaps": [
    "A clear notification procedure for AI systems and cross-border cooperation mechanisms are missing or unclear."
  ],
  "confidence": "medium"
}
```

**Citation check:** G05 p.48 (Directive (EU) 2022/2555 (NIS2) on a high common level of cy) → verified


### Data-Protection Authority agent

**Received:** An anonymous tip: during the incident a misconfigured logging server exposed subscriber location records (about 120,000 subscribers) to the internet for an unknown period.

**Retrieved:** G04 p.59 (0.5709), G04 p.102 (0.5708), G12 p.22 (0.5265), G05 p.51 (0.522)

```json
{
  "assessment": "An anonymous tip suggests a misconfigured logging server exposed subscriber location records of about 120,000 subscribers to the internet for an unknown period, potentially violating data protection regulations and privacy rights. This incident requires swift notification to the relevant authorities and affected parties, as well as a review of cross-border cooperation mechanisms and notification procedures.",
  "reasoning": [
    "The incident involves a potential data breach that could affect privacy rights.",
    "The notification procedures and cross-border cooperation mechanisms need to be reviewed and improved to ensure compliance with data protection regulations."
  ],
  "actions": [
    {
      "action": "Notify the affected subscribers and relevant authorities about the data breach.",
      "owner": "SOC|REGULATOR|DPA|CERT",
      "deadline": "Within 24 hours"
    },
    {
      "action": "Review and improve notification procedures and cross-border cooperation mechanisms.",
      "owner": "SOC|REGULATOR|DPA|CERT",
      "deadline": "Within 7 days"
    }
  ],
  "policy_refs": [
    {
      "ref": "G05 p.51 (Directive (EU) 2022/2555 (NIS2) on a high common level of cybersecurity)",
      "point": "The cybersecurity authorities shall provide to the competent authorities under Directive (EU) 2022/2557 information about significant incidents, incidents, cyber threats and near misses notified in accordance with paragraph 1 of this Article and with Article 30 by entities identified as critical entities under Directive (EU) 2022/2557."
    },
    {
      "ref": "G12 p.22 (African Union Convention on Cyber Security and Personal Data)",
      "point": "In cases of emergency, where the processing or use of personal data results in violation of fundamental rights and freedoms, the national protection authority may, after adversary proceedings, decide as follows: a) Discontinuation of data processing; b) Blocking of some of the personal data processed; c) Temporary or permanent prohibition of any processing at variance with the provisions of this Convention."
    }
  ],
  "requests": [
    {
      "to": "SOC|REGULATOR|DPA|CERT",
      "request": "Information about the notification procedures and cross-border cooperation mechanisms, and any existing gaps or issues."
    }
  ],
  "gaps": [
    "A clear notification procedure for AI systems and cross-border cooperation mechanisms are missing or unclear."
  ],
  "confidence": "medium"
}
```

**Citation check:** G05 p.51 (Directive (EU) 2022/2555 (NIS2) on a high common level of cybersecurity) → verified, G12 p.22 (African Union Convention on Cyber Security and Personal Data) → verified


### Policy & Legal Adviser agent (coordinator)

**Retrieved:** G04 p.102 (0.662), G08 p.19 (0.6078), G13 p.56 (0.5966), G10 p.4 (0.5807), G02 p.38 (0.565), G05 p.55 (0.5479)

```json
{
  "summary": "The agents have identified gaps in notification procedures and cross-border cooperation mechanisms. The SOC, REGULATOR, DPA, and CERT have all highlighted the need for clear procedures and mechanisms to address incidents involving AI systems and data breaches. The REGULATOR has also noted the need for effective incident management and cross-border cooperation.",
  "conflicts": [
    "SOC's request for independent validation and rollback plan conflicts with CERT's request for further information on containment measures and coordination with affected operators."
  ],
  "unclear_responsibilities": [
    "It is unclear who should lead the notification of serious incidents involving AI systems and data breaches, as all relevant authorities (SOC, REGULATOR, DPA, CERT) are involved and have overlapping responsibilities."
  ],
  "policy_gaps": [
    {
      "gap": "Clear notification procedures for AI systems and cross-border cooperation mechanisms are missing or unclear.",
      "global_example": "Regulation (EU) 2022/2555 (NIS2) on a high common level of cybersecurity, which requires entities to notify significant incidents, cyber threats, and near misses to the CSIRTs or competent authorities, and outlines the procedures for processing these notifications.",
      "ref": "G05 p.55 (Directive (EU) 2022/2555 (NIS2) on a high common level of cybersecurity)",
      "recommendation": "Develop clear and standardized notification procedures for AI systems and cross-border cooperation mechanisms, as outlined in the Directive (EU) 2022/2555 (NIS2)."
    },
    {
      "gap": "Cross-border cooperation mechanisms are missing or unclear.",
      "global_example": "Directive (EU) 2022/2555 (NIS2) on a high common level of cybersecurity, which requires entities to notify significant incidents, cyber threats, and near misses to the CSIRTs or competent authorities, and outlines the procedures for processing these notifications.",
      "ref": "G05 p.55 (Directive (EU) 2022/2555 (NIS2) on a high common level of cybersecurity)",
      "recommendation": "Establish clear cross-border cooperation mechanisms and procedures for handling incidents involving AI systems and data breaches, as outlined in the Directive (EU) 2022/2555 (NIS2)."
    }
  ],
  "standards_gaps": [
    "There is no specific technical standard or evaluation practice for the validation and rollback plan of AI models, as mentioned in the NIST AI Risk Management Framework (AI RMF 1.0)."
  ],
  "priorities_next_round": [
    "Develop clear and standardized notification procedures for AI systems and cross-border cooperation mechanisms, as outlined in the Directive (EU) 2022/2555 (NIS2)."
  ]
}
```

**Citation check:** G05 p.55 (Directive (EU) 2022/2555 (NIS2) on a high common level of cybersecurity) → verified, G05 p.55 (Directive (EU) 2022/2555 (NIS2) on a high common level of cybersecurity) → verified


## Round 4 (T+06:00)


### Operator Security Operations Centre (SOC) agent

**Received:** Attack traffic is subsiding after manual filtering; services are 95% restored. | msg from REGULATOR: Further information on the new attack variant and the impact on the network.

**Retrieved:** G05 p.14 (0.6362), G05 p.12 (0.5936), G08 p.44 (0.5918), G08 p.44 (0.5916)

```json
{
  "assessment": "Attack traffic is subsiding, but services are still 95% restored. The regulator requires further information on the new attack variant and its impact, as well as on containment measures and coordination with affected operators. The SOC has identified gaps in notification procedures and cross-border cooperation mechanisms, and the priorities for the next round include developing clear and standardized notification procedures and cross-border cooperation mechanisms as outlined in the Directive (EU) 2022/2555 (NIS2).",
  "reasoning": [
    "Attack traffic is subsiding but services are not fully restored.",
    "The regulator needs further information on the attack and containment measures.",
    "The SOC has identified gaps in notification procedures and cross-border cooperation mechanisms."
  ],
  "actions": [
    {
      "action": "Develop clear and standardized notification procedures for AI systems and cross-border cooperation mechanisms as per NIS2 Directive.",
      "owner": "SOC",
      "deadline": "Within 1 week"
    }
  ],
  "policy_refs": [
    {
      "ref": "G05 p.14",
      "point": "Member States and the relevant Union institutions, bodies, offices and agencies should cooperate at technical, operational and political level to properly coordinate the response across the Union."
    },
    {
      "ref": "G05 p.12",
      "point": "Member States should adopt policies on the promotion of active cyber protection as part of a wider defensive strategy."
    },
    {
      "ref": "G08 p.44",
      "point": "Address many other types of risks – frameworks like those mentioned above may inform security and privacy considerations in the MAP, MEASURE, and MANAGE functions of the AI RMF."
    }
  ],
  "requests": [
    {
      "to": "REGULATOR",
      "request": "Further information on the new attack variant, its impact, containment measures, and cross-border cooperation mechanisms."
    }
  ],
  "gaps": [
    "A clear and standardized notification procedure for AI systems and cross-border cooperation mechanisms is missing."
  ],
  "confidence": "medium"
}
```

**Citation check:** G05 p.14 → verified, G05 p.12 → verified, G08 p.44 → verified


### National Telecom Regulator agent

**Received:** The ministry asks for a lessons-learned report by tomorrow, and asks whether the same AI detector can be reused by the national electricity utility's network. | msg from SOC: Clarify the roles and responsibilities in cross-border cooperation mechanisms.

**Retrieved:** G13 p.56 (0.6339), G05 p.14 (0.6334), G05 p.6 (0.6176), U01 p.22 (0.6138)

```json
{
  "assessment": "The national electricity utility is seeking to reuse an AI detector developed for the telecommunications sector, which could lead to potential gaps in cybersecurity if not properly managed. This situation is relevant to the national telecommunications regulator's mandate as it involves cross-border cooperation and the need for effective incident management and notification procedures.",
  "reasoning": [
    "The reuse of AI detectors across sectors requires clear guidelines and cooperation mechanisms to prevent security risks.",
    "The regulator needs to ensure that the reuse of AI systems complies with Directive (EU) 2022/2555 (NIS2) and other relevant policies.",
    "The regulator should coordinate with the electricity utility to establish clear procedures for cross-border cooperation and incident management."
  ],
  "actions": [
    {
      "action": "Clarify the roles and responsibilities for the reuse of AI detectors between the telecommunications and electricity sectors.",
      "owner": "SOC",
      "deadline": "Within 1 week"
    }
  ],
  "policy_refs": [
    {
      "ref": "G05 p.6 (Directive (EU) 2022/2555 (NIS2) on a high common level of cy)",
      "point": "Where sector-specific Union legal acts require or provide incentives to entities to notify significant cyber threats, Member States should also establish cooperation arrangements for that purpose."
    },
    {
      "ref": "G13 p.56 (African Union Continental Artificial Intelligence Strategy)",
      "point": "Mitigating AI security and safety risks requires concerted global efforts, building regional and national capabilities to assess and identify, protect, detect, respond and recover from threats in digital space, political systems and societies and AI integration in physical systems and critical infrastructure."
    }
  ],
  "requests": [
    {
      "to": "CERT",
      "request": "Provide information on containment measures and coordination with affected operators for the reuse of AI detectors."
    },
    {
      "to": "DPA",
      "request": "Clarify the legal framework for the reuse of AI detectors and its alignment with the UAE National Strategy for Artificial Intelligence 2031."
    }
  ],
  "gaps": [
    "A clear and standardized notification procedures for AI systems and cross-border cooperation mechanisms, as outlined in the Directive (EU) 2022/2555 (NIS2)."
  ],
  "confidence": "medium"
}
```

**Citation check:** G05 p.6 (Directive (EU) 2022/2555 (NIS2) on a high common level of cy) → verified, G13 p.56 (African Union Continental Artificial Intelligence Strategy) → verified


### Data-Protection Authority agent

**Received:** Journalists ask whether 'the AI failed' and whether affected subscribers will be told.

**Retrieved:** G04 p.106 (0.6655), G04 p.41 (0.654), G10 p.9 (0.6429), G05 p.24 (0.6296)

```json
{
  "assessment": "The AI system involved in the breach is considered high-risk and requires immediate attention. The SOC, REGULATOR, DPA, and CERT have highlighted the need for clear procedures and mechanisms to address incidents involving AI systems and data breaches, as outlined in the Directive (EU) 2022/2555 (NIS2).",
  "reasoning": [
    "The AI system is high-risk and requires immediate attention.",
    "Clear procedures and mechanisms are needed to address AI system incidents and data breaches."
  ],
  "actions": [
    {
      "action": "Review and update notification procedures and cross-border cooperation mechanisms in line with Directive (EU) 2022/2555 (NIS2).",
      "owner": "SOC|REGULATOR|DPA|CERT",
      "deadline": "Within 1 week"
    }
  ],
  "policy_refs": [
    {
      "ref": "G04 p.106",
      "point": "They shall put in place adequate and effective cybersecurity measures to protect the security and confidentiality of the information and data obtained, and shall delete the data collected as soon as it is no longer needed for the purpose for which it was obtained, in accordance with applicable Union or national law."
    },
    {
      "ref": "G04 p.41",
      "point": "In such cases, the procedure regarding mutual assistance in cross-border cases in Chapter VI of Regulation (EU) 2019/1020 should apply mutatis mutandis."
    },
    {
      "ref": "Directive (EU) 2022/2555 (NIS2) p.24",
      "point": "Entities should be encouraged and assisted by Member States to collectively leverage their individual knowledge and practical experience at strategic, tactical and operational levels with a view to enhancing their capabilities to adequately prevent, detect, respond to or recover from incidents or to mitigate their impact."
    }
  ],
  "requests": [
    {
      "to": "SOC|REGULATOR|DPA|CERT",
      "request": "Information on existing guidance and best practices for AI system incidents and data breach notifications, as well as any specific requirements under Directive (EU) 2022/2555 (NIS2)."
    }
  ],
  "gaps": [
    "A clear and standardized notification procedures for AI systems and cross-border cooperation mechanisms are missing or unclear."
  ],
  "confidence": "medium"
}
```

**Citation check:** G04 p.106 → verified, G04 p.41 → verified, Directive (EU) 2022/2555 (NIS2) p.24 → no-source-id


### National Cybersecurity Agency / CERT agent

**Received:** Attack command servers are traced to hosting providers in a jurisdiction with which there is no mutual legal assistance agreement. | msg from SOC: Provide information on the potential unseen attack type and how to proceed with containment measures. | msg from REGULATOR: Further information on containment measures and coordination with the affected operators.

**Retrieved:** G05 p.44 (0.6661), G05 p.9 (0.659), G12 p.28 (0.6331), G12 p.31 (0.6295)

```json
{
  "assessment": "Attack command servers traced to a jurisdiction without a mutual legal assistance agreement, indicating a need for swift coordination and potential legal challenges in cross-border enforcement. This situation is critical for the national CERT's mandate as it requires immediate containment measures and cross-border cooperation, especially given the lack of established mechanisms and agreements.",
  "reasoning": [
    "The attack originates from a jurisdiction without a mutual legal assistance agreement, highlighting the need for swift action and coordination with international partners.",
    "The lack of established mechanisms and agreements makes the containment and response process more complex and challenging, necessitating clear procedures and mechanisms as outlined in the NIS2 Directive."
  ],
  "actions": [
    {
      "action": "Inform the affected operators and provide further information on containment measures.",
      "owner": "CERT",
      "deadline": "Within 1 hour"
    },
    {
      "action": "Coordinate with the affected operators and the REGULATOR to develop clear procedures for cross-border cooperation.",
      "owner": "CERT",
      "deadline": "Within 1 hour"
    }
  ],
  "policy_refs": [
    {
      "ref": "G05 p.44",
      "point": "to discuss and identify further forms of operational cooperation, including in relation to: (i) categories of cyber threats and incidents; (ii) early warnings; (iii) mutual assistance; (iv) principles and arrangements for coordination in response to cross-border risks and incidents; (v) contribution to the national large-scale cybersecurity incident and crisis response plan referred to in Article 9(4) at the request of a Member State;"
    },
    {
      "ref": "G05 p.9",
      "point": "In order to facilitate cross-border cooperation and communication among authorities and to enable this Directive to be implemented effectively, it is necessary for each Member State to designate a single point of contact responsible for coordinating issues related to the security of network and"
    },
    {
      "ref": "G12 p.28",
      "point": "Legislation against cybercrime Each State Party shall adopt such legislative and/or regulatory measures as it deems effective by considering as substantive criminal offences acts which affect the confidentiality, integrity, availability and survival of information and"
    },
    {
      "ref": "G12 p.31",
      "point": "State Parties shall encourage the establishment of institutions that exchange information on cyber threats and vulnerability assessment such as the Computer Emergency Response Team (CERT) or the Computer Security Incident Response Teams (CSIRTs)."
    }
  ],
  "requests": [
    {
      "to": "SOC",
      "request": "Information on the potential unseen attack type and how to proceed with containment measures."
    },
    {
      "to": "REGULATOR",
      "request": "Further information on containment measures and coordination with the affected operators."
    }
  ],
  "gaps": [
    "The lack of established mechanisms and agreements for cross-border cooperation, as mentioned in G05 p.44 and G05 p.9."
  ],
  "confidence": "medium"
}
```

**Citation check:** G05 p.44 → verified, G05 p.9 → verified, G12 p.28 → verified, G12 p.31 → verified


### Policy & Legal Adviser agent (coordinator)

**Retrieved:** G04 p.41 (0.6835), G05 p.7 (0.6611), G13 p.18 (0.6601), G08 p.29 (0.6551), G10 p.11 (0.6359), U01 p.22 (0.6273)

```json
{
  "summary": "The SOC, REGULATOR, DPA, and CERT have identified gaps in notification procedures and cross-border cooperation mechanisms. The SOC and REGULATOR have proposed developing clear and standardized procedures, while the DPA and CERT have emphasized the need for immediate containment measures and cross-border cooperation. The SOC and REGULATOR have also requested further information on containment measures and coordination with affected operators.",
  "conflicts": [
    "The SOC and REGULATOR have proposed developing clear and standardized procedures, while the DPA and CERT have emphasized the need for immediate containment measures and cross-border cooperation."
  ],
  "unclear_responsibilities": [
    "It is unclear who should lead the development of clear and standardized notification procedures and cross-border cooperation mechanisms, especially when one incident involves multiple sectors and jurisdictions."
  ],
  "policy_gaps": [
    {
      "gap": "A clear and standardized notification procedure for AI systems and cross-border cooperation mechanisms, as outlined in the Directive (EU) 2022/2555 (NIS2).",
      "global_example": "The SOC and REGULATOR have proposed developing clear and standardized procedures, while the DPA and CERT have emphasized the need for immediate containment measures and cross-border cooperation.",
      "ref": "G05 p.14, G05 p.12, G08 p.44, G04 p.41, G04 p.106, G04 p.41, G13 p.56, G12 p.28, G12 p.31",
      "recommendation": "Develop clear and standardized notification procedures and cross-border cooperation mechanisms in line with Directive (EU) 2022/2555 (NIS2) and other relevant policies."
    },
    {
      "gap": "Cross-border cooperation mechanisms for the reuse of AI detectors between the telecommunications and electricity sectors.",
      "global_example": "The SOC, REGULATOR, DPA, and CERT have highlighted the need for clear procedures and mechanisms to address incidents involving AI systems and data breaches.",
      "ref": "G05 p.6, G13 p.56, G04 p.106, G04 p.41, G04 p.41, G04 p.41, G04 p.41, G12 p.28, G12 p.31",
      "recommendation": "Clarify the roles and responsibilities for the reuse of AI detectors between the telecommunications and electricity sectors."
    }
  ],
  "standards_gaps": [
    "Technical standard or evaluation practice that is missing for the reuse of AI detectors between the telecommunications and electricity sectors."
  ],
  "priorities_next_round": [
    "Develop clear and standardized notification procedures and cross-border cooperation mechanisms in line with Directive (EU) 2022/2555 (NIS2).",
    "Clarify the roles and responsibilities for the reuse of AI detectors between the telecommunications and electricity sectors."
  ]
}
```

**Citation check:** G05 p.14, G05 p.12, G08 p.44, G04 p.41, G04 p.106, G04 p.41, G13 p.56, G12 p.28, G12 p.31 → source-retrieved-page-mismatch, G05 p.6, G13 p.56, G04 p.106, G04 p.41, G04 p.41, G04 p.41, G04 p.41, G12 p.28, G12 p.31 → source-retrieved-page-mismatch
