from typing import Optional

TEMPLATES = {
    "bangla": {
        "bootcamp": "আসসালামু আলাইকুম{name_part}, BIAI-এর AI বুটক্যাম্প ও মাস্টারক্লাসে আগ্রহ প্রকাশের জন্য ধন্যবাদ! আমাদের বুটক্যাম্পের ফি ৩,৫০০ টাকা। ক্লাসগুলো লাইভ অনলাইনে পরিচালিত হয় এবং প্রতিটি ক্লাসের রেকর্ডিং ও রিসোর্সের লাইফটাইম অ্যাক্সেস দেওয়া হয়। আপনি কি মাস্টারক্লাস বা আসন্ন বুটক্যাম্পে অংশ নিতে চান? আপনার হোয়াটসঅ্যাপ নম্বরটি জানালে আমরা ক্লাসরুম লিংক ও বিস্তারিত পাঠিয়ে দিচ্ছি।",
        "fellowship": "আসসালামু আলাইকুম{name_part}, BIAI AI ফেলোশিপ প্রোগ্রামে আগ্রহ প্রকাশের জন্য ধন্যবাদ! এটি আমাদের ৬ মাসের একটি সমন্বিত ক্যারিয়ার ট্র্যাক, যেখানে হ্যান্ডস-অন প্রজেক্টের মাধ্যমে AI শেখানো হয়। পরবর্তী ব্যাচের ভর্তি চলছে এবং কিস্তিতে ফি দেওয়ার সুবিধা রয়েছে। আপনি আপনার প্রোফাইল বা হোয়াটসঅ্যাপ নম্বর শেয়ার করলে আমাদের টিম বিস্তারিত জানিয়ে যোগাযোগ করবে।",
        "corporate": "আসসালামু আলাইকুম{name_part}, আপনার প্রতিষ্ঠানের জন্য BIAI করপোরেট AI ট্রেনিং নিয়ে যোগাযোগ করার জন্য ধন্যবাদ! আমরা অনসাইট এবং অনলাইন উভয় মাধ্যমেই টিম ট্রেনিং পরিচালনা করে থাকি এবং গ্রুপ ডিসকাউন্টের সুবিধা রয়েছে। আপনার সুবিধাজনক একটি সময় জানালে আমাদের করপোরেট টিম একটি সংক্ষিপ্ত আলোচনা সেশন আয়োজন করবে।",
        "support": "আসসালামু আলাইকুম{name_part}, আপনার সমস্যাটির কথা জানানোর জন্য আন্তরিক ধন্যবাদ। বিষয়টি আমরা সর্বোচ্চ গুরুত্ব দিয়ে দেখছি এবং দ্রুত সমাধানের জন্য সংশ্লিষ্ট টিমের কাছে পাঠানো হয়েছে। আমাদের সাপোর্ট টিম খুব শীঘ্রই আপনার সাথে যোগাযোগ করবে।",
        "job_seeker": "আসসালামু আলাইকুম{name_part}, BIAI-তে ক্যারিয়ার গড়ার আগ্রহের জন্য ধন্যবাদ। অনুগ্রহ করে আপনার আপডেট করা সিভি (CV) ও পোর্টফোলিও careers@biai.edu.bd ঠিকানায় ইমেইল করুন।",
        "spam": "আপনার বার্তার জন্য ধন্যবাদ। BIAI শুধুমাত্র শিক্ষামূলক ও পেশাদার AI ট্রেনিং সেবা প্রদান করে।",
        "unknown": "আসসালামু আলাইকুম{name_part}, BIAI-তে যোগাযোগ করার জন্য ধন্যবাদ! আমাদের AI কোর্স, ফি এবং মাস্টারক্লাসের সময়সূচি সম্পর্কে বিস্তারিত জানতে আমরা আপনাকে সহযোগিতা করতে প্রস্তুত। আপনি কি নির্দিষ্ট কোনো কোর্স (বুটক্যাম্প / ফেলোশিপ / করপোরেট) সম্পর্কে জানতে চাচ্ছেন?"
    },
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
    lang = reply_language if reply_language in ["bangla", "banglish", "english"] else "bangla"
    name_part = f" {name.strip()}" if name and name.strip() else ""

    lang_dict = TEMPLATES.get(lang, TEMPLATES["bangla"])

    # If enquiry_type is support, spam, or job_seeker, prioritize that
    if enquiry_type in ["support", "spam", "job_seeker"]:
        tpl = lang_dict.get(enquiry_type, lang_dict["unknown"])
    else:
        # For sales inquiries, match by interest
        tpl = lang_dict.get(interest, lang_dict["unknown"])

    return tpl.format(name_part=name_part)

