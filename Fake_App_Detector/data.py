# Official PhonePe app details
OFFICIAL_APP = {
    "name": "PhonePe: UPI, Payment, Recharge",
    "package": "com.phonepe.app",
    "publisher": "PhonePe Pvt. Ltd",
    "icon_path": "icons/phonepe.png"
}

# Some sample candidate apps (mix of real-like and fake-like)
CANDIDATE_APPS = [
    {
        "name": "PhonePe: UPI, Payment, Recharge",
        "package": "com.phonepe.app",
        "publisher": "PhonePe Pvt. Ltd",
        "icon_path": "icons/phonepe.png",
        "description": "Official PhonePe app for UPI, recharges and payments.",
        "permissions": ["INTERNET"]
    },
    {
        "name": "Phone Pe UPI Rewards",
        "package": "com.phonepe.upi.rewards.free",
        "publisher": "XYZ Tech Ltd",
        "icon_path": "icons/phonepe_fake1.png",
        "description": "Get free rewards and cashback by using this PhonePe rewards app.",
        "permissions": ["INTERNET", "READ_SMS", "READ_CONTACTS"]
    },
    {
        "name": "Ph0nePe UPI Pay",
        "package": "com.ph0nepe.upi",
        "publisher": "Random Dev",
        "icon_path": "icons/phonepe_fake2.png",
        "description": "Instant UPI money transfer, bonus rewards, earn more money easily.",
        "permissions": ["INTERNET", "READ_SMS"]
    },
    {
        "name": "UPI Payments & Wallet",
        "package": "com.upi.wallet.app",
        "publisher": "SafePay Ltd",
        "icon_path": "icons/generic_upi.png",
        "description": "Generic UPI wallet for simple payments.",
        "permissions": ["INTERNET"]
    },
    {
        "name": "PhonePay Cashback Offer 2025",
        "package": "com.phonepay.cashback2025.free",
        "publisher": "Bonus Apps Inc",
        "icon_path": "icons/phonepe_fake3.png",
        "description": "Win cashback, rewards and lottery offers by using this PhonePay app.",
        "permissions": ["INTERNET", "READ_SMS", "READ_CALL_LOG"]
    },
    {
        "name": "Google Pay: Secure UPI Payments",
        "package": "com.google.android.apps.nbu.paisa.user",
        "publisher": "Google LLC",
        "icon_path": "icons/gpay.png",
        "description": "Official Google Pay app for secure UPI, recharges and payments.",
        "permissions": ["INTERNET"]
    },
    {
        "name": "BHIM – Making India Cashless",
        "package": "in.org.npci.upiapp",
        "publisher": "NPCI",
        "icon_path": "icons/bhim.png",
        "description": "Official BHIM UPI app.",
        "permissions": ["INTERNET"]
    },
    {
        "name": "PhonePe Bonus Money Trick",
        "package": "com.phonepe.bonus.trick2025",
        "publisher": "FreeCash Devs",
        "icon_path": "icons/phonepe_fake4.png",
        "description": "Use this PhonePe bonus trick app to double your money and win lottery rewards.",
        "permissions": ["INTERNET", "READ_SMS", "READ_CONTACTS", "READ_CALL_LOG"]
    },
    {
        "name": "PhonePe Free Cashback Pro",
        "package": "com.phonepe.cashback.pro.free",
        "publisher": "CashBack Pro Ltd",
        "icon_path": "icons/phonepe_fake5.png",
        "description": "Pro cashback app for PhonePe users to get instant rewards and bonuses.",
        "permissions": ["INTERNET", "READ_SMS"]
    }
]

# Fast lookup by package id
APP_INDEX = {app["package"]: app for app in CANDIDATE_APPS}

