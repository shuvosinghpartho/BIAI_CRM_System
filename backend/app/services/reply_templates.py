from typing import Optional

TEMPLATES = {
    "banglish": {
        "bootcamp": "Assalamualaikum{name_part}, BIAI er 3-day AI Bootcamp niye interest jananor jonno dhonnobad! Amader upcoming bootcamp er fee 3,500 BDT. Class gula live online e hoy ebong shob class er full recording & lifetime resources paben. Apnar seat confirm korte ba payment details jante chaile kindly janan, amra link pathiye dicchi.",
        "fellowship": "Assalamualaikum{name_part}, BIAI AI Fellowship program e agroho prokash korar jonno dhonnobad! Eta amader comprehensive 6-month hands-on career track, jekhane coding & non-coding professional shobaikei guide kora hoy. Next batch er admission open ache ebong 2 instalment e payment suvidha royeche. Apnar profile share korle amader team call kore bistarto janabe.",
        "corporate": "Assalamualaikum{name_part}, apnar protishthaner jonno BIAI corporate AI training niye jogajog korar jonno dhonnobad! Amra customized online ebong onsite duivabe-i team training provide kore thaki, ebong group discount er suvidha ache. Apnader team size o requirements niye amader team er shathe ekta quick discussion call schedule korte apnar shubidajonok somoy ta janan please.",
        "support": "Assalamualaikum{name_part}, apnar shomosshar kotha jananor jonno dhonnobad. Amra bishoyti ontorikbhabe dekhesi ebong priority hishebe solve korar jonno shathe shathe amader support team ke forward korechi. Amader team khub shobdo-i apnar shathe call/message e jogajog korbe.",
        "job_seeker": "Assalamualaikum{name_part}, BIAI te carrier gore tolar agrohe dhonnobad. Kindly apnar updated CV ebong portfolio careers@biai.edu.bd te email kore din. Shortlist hole amader HR team jogajog korbe.",
        "spam": "Dhonnobad apnar message er jonno. BIAI sudhumatro educational o professional AI training provide kore.",
        "unknown": "Assalamualaikum{name_part}, BIAI te jogajog korar jonno dhonnobad! Amader AI training programs, course fee ebong batch schedule somporke bistarto jante amader team apnake help korte prostut. Apni ki specific kono course (Bootcamp / Fellowship / Corporate) somporke jante chassen?"
    },
    "english": {
        "bootcamp": "Hello{name_part}, thank you for reaching out regarding BIAI's 3-Day AI Bootcamp! The fee for our upcoming hands-on bootcamp is 3,500 BDT. All sessions are live interactive sessions with lifetime recorded access provided. Please let us know if you would like the direct payment link to reserve your seat.",
        "fellowship": "Hello{name_part}, thank you for your interest in the BIAI AI Fellowship! This 6-month intensive program is tailored for both technical and non-technical professionals aiming to master AI in their careers. We also offer 2-part instalment options. Would you like to schedule a quick consultation call with an advisor?",
        "corporate": "Hello{name_part}, thank you for considering BIAI for your team's AI training! We offer customized on-site and online corporate upskilling programs with group pricing. Could you let us know a convenient time this week for a 15-minute alignment call with our corporate training lead?",
        "support": "Hello{name_part}, thank you for contacting us. We sincerely apologize for any inconvenience caused. Our support team is actively reviewing your request and will reach out immediately to resolve this for you.",
        "job_seeker": "Hello{name_part}, thank you for your interest in joining the BIAI team. Please forward your updated CV and portfolio to careers@biai.edu.bd. Our recruitment team will review your application.",
        "spam": "Thank you for contacting BIAI. We do not accept promotional or unsolicited offers.",
        "unknown": "Hello{name_part}, thank you for reaching out to BIAI! We would love to assist you with our AI bootcamps, fellowship programs, and corporate training. Could you please share a bit more detail about your background or requirements so we can guide you best?"
    }
}

def get_template_reply(
    reply_language: str,
    interest: str = "unknown",
    enquiry_type: str = "sales",
    name: Optional[str] = None
) -> str:
    lang = "english" if reply_language == "english" else "banglish"
    name_part = f" {name.strip()}" if name and name.strip() else ""

    lang_dict = TEMPLATES.get(lang, TEMPLATES["banglish"])

    # If enquiry_type is support, spam, or job_seeker, prioritize that
    if enquiry_type in ["support", "spam", "job_seeker"]:
        tpl = lang_dict.get(enquiry_type, lang_dict["unknown"])
    else:
        # For sales inquiries, match by interest
        tpl = lang_dict.get(interest, lang_dict["unknown"])

    return tpl.format(name_part=name_part)

