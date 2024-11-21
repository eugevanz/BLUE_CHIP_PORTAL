from dash import html

from utils import sign_out_button

messages = [
    ('Written by Super User on 08 March 2021. Posted in Blog',
     'Understanding Inflation: What It Means for Your Savings',
     'Inflation can significantly impact the value of your savings over time. This '
     'article explores what inflation is, how it’s measured, and why it matters for '
     'anyone with long-term financial goals. We’ll also offer tips on how to protect your '
     'investments and savings from the negative effects of inflation.'),
    ('Written by Super User on 15 June 2020. Posted in Blog',
     'The Basics of Stock Market Investing',
     'Whether you’re new to investing or looking to improve your portfolio, understanding '
     'the basics of the stock market is essential. In this article, we break down key '
     'concepts like stock prices, dividends, and market trends to help you get started on '
     'the right foot.'),
    ('Written by Super User on 22 November 2019. Posted in Blog',
     'How to Build a Balanced Investment Portfolio',
     'Creating a diversified investment portfolio is one of the most effective strategies '
     'for long-term growth. Learn about the importance of balancing risk with reward, '
     'and how to allocate assets across stocks, bonds, and other investment types to meet '
     'your financial goals.'),
    ('Written by Super User on 05 February 2022. Posted in Blog',
     'Retirement Planning: Steps to Secure Your Future',
     'Retirement planning can seem overwhelming, but starting early can make a huge '
     'difference. This guide walks you through the key steps in building a retirement '
     'strategy, from choosing the right savings accounts to understanding pension plans '
     'and Social Security benefits.'),
    ('Written by Super User on 30 September 2023. Posted in Blog',
     'The Role of Cryptocurrency in Modern Finance',
     'Cryptocurrency is becoming an increasingly popular alternative to traditional '
     'finance. This article explores the rise of digital currencies like Bitcoin and '
     'Ethereum, their potential benefits and risks, and what they mean for the future of '
     'global financial systems.')
]

faqs = [
    ('How do I create an account?',
     'To create an account, get in contact with one of our consultants. Once you have an account with us, check your email for a confirmation link. Click it to activate your account, and you’re all set!',
     'create-an-account'),
    ('How can I reset my password?',
     'No worries! You don’t have a password to reset! This app uses a One-Time Pin to sign in, eliminating the need for passwords. Be sure to check your spam folder if you don’t see the email right away!',
     'reset-my-password'),
    ('How do I update my contact details (email, phone number, etc.)?',
     'Updating your details is simple, but it needs to be done through our account management team. Just give us a call, and submit a request to update your email, phone number, or other personal details. Our team will process the changes, and you’ll receive a confirmation once they’re complete.',
     'my-contact-details'),
    ('What should I do if I can’t log in?',
     'If you’re having trouble logging in, double-check that you’re entering the correct email. If that doesn’t work, feel free to reach out to us via the support form, and we’ll be happy to assist.',
     'cant-log-in'),
    ('What information do I need to provide when contacting support?',
     'When submitting a support request, it helps to include as much detail as possible about your issue. Provide the exact steps you took when the problem occurred, any error messages you received, and screenshots or recordings if possible. This will help us resolve your issue faster!',
     'contacting-support'),
    ('How do you protect my personal data?',
     'Your privacy is important to us. We use industry-standard encryption protocols and secure servers to protect your personal information.',
     'my-personal-data'),
    ('What should I do if the portal is not loading properly?',
     'If the portal isn’t loading, try refreshing your browser or clearing your cache and cookies. If the issue persists, try switching browsers or disabling any browser extensions that might be interfering.',
     'not-loading-properly'),
    ('How can I clear my browser’s cache and cookies to resolve issues?',
     'To clear your cache and cookies, go to your browser settings, find the “Privacy” section, and look for “Clear Browsing Data.” Select “Cache” and “Cookies,” and click “Clear Data.” This often resolves many issues with page loading.',
     'to-resolve-issues'),
    ('Why am I getting error messages during login or while using services?',
     'Error messages can sometimes occur due to incorrect login credentials or a temporary server issue. Double-check your login details and try again. If the issue continues, please submit a support request so we can look into it for you.',
     'using-services')
]

investment_faqs = [
    ('How do I start investing?',
     'To start investing, you’ll need to open an investment account. Once your account is set up, you can deposit funds and choose from various investment options, such as stocks, bonds, mutual funds, or ETFs. If you’re unsure where to begin, it’s a good idea to determine your financial goals and risk tolerance before selecting investments.',
     'start-investing'),
    ('Can I get advice on which investments to choose?',
     'Yes, you can receive advice on your investment options. Our team offers personalized investment recommendations based on your financial goals, risk tolerance, and time horizon. You can also schedule a consultation with an advisor for more detailed guidance.',
     'investments-to-choose'),
    ('How can I track my investments?',
     'You can track your investments through your account dashboard, where you’ll find real-time updates on performance, gains, and losses. You can also set up alerts to notify you of significant changes in your portfolio or the market.',
     'my-investments'),
    (
        'What’s the difference between a conservative, balanced, and aggressive portfolio?',
        'Conservative portfolios are lower risk and focus on preserving capital by investing in safer assets like bonds. Balanced portfolios aim to provide moderate growth by combining stocks and bonds, balancing risk and return. Aggressive portfolios carry higher risk but offer higher potential returns, primarily investing in stocks or high-growth assets.',
        'aggressive-portfolio'),
    ('What does diversification mean, and why is it important?',
     'Diversification means spreading your investments across different asset classes (like stocks, bonds, and real estate) to reduce risk. It’s important because it helps protect your portfolio from significant losses if one type of investment performs poorly, thus balancing overall returns.',
     'is-it-important'),
    ('What level of risk should I expect with my investments?',
     'The level of risk depends on the types of investments you choose and your investment strategy. Conservative investments tend to be lower risk, while aggressive investments come with higher risk but higher potential rewards. We help you align your risk tolerance with your investment goals.',
     'with-my-investments'),
    ('Is there a limit on how much I can invest?',
     'There is generally no upper limit on how much you can invest, though some investment products may have minimum investment requirements. Additionally, certain tax-advantaged accounts (like IRAs) have annual contribution limits based on government regulations.',
     'can-invest'),
    ('Can I withdraw money from my investments?',
     'Yes, you can withdraw money from your investments. However, the process and timeframe can vary depending on the type of investments and whether they are in tax-advantaged accounts. Keep in mind that withdrawing funds may impact your investment strategy and long-term growth potential.',
     'money-from-my-investments'),
    ('How can I add money to my investment account?',
     'To add money to your investment account, log in, go to the “Funding” section, and select your preferred deposit method. You can typically transfer funds from your bank account or set up recurring contributions.',
     'my-investment-account'),
    ('Do I need to report my investment earnings for tax purposes?',
     'Yes, investment earnings are typically subject to taxes. You’ll receive documentation outlining your earnings (such as dividends, interest, and capital gains) to help you file your taxes. Specific tax treatment may depend on the type of account and investment.',
     'for-tax-purposes'),
    ('Do you offer socially responsible or sustainable investment options?',
     'Yes, we offer socially responsible and sustainable investment options that focus on companies and funds aligned with environmental, social, and governance (ESG) criteria. These portfolios allow you to invest in line with your values while aiming for financial returns.',
     'investment-options'),
    ('Can I customize my portfolio to focus on sustainability?',
     'Absolutely. You can work with our team to tailor your portfolio to prioritize sustainable and socially responsible investments. We offer a range of ESG-focused funds that you can incorporate into your investment strategy.',
     'on-sustainability'),
    ('Who can I contact if I have questions about my investments?',
     'You can reach out to our support team for any investment-related questions. We also offer access to financial advisors who can help address your concerns and provide personalized guidance.',
     'about-my-investments'),
    ('How do I schedule a consultation with an investment advisor?',
     'To schedule a consultation, simply log in to your account and navigate to the “Consultation” section. From there, you can choose a time that works for you, and one of our advisors will reach out to provide personalized investment advice.',
     'an-investment-advisor')
]


def client_menu_card(profile):
    return html.Div([
        html.Div([
            html.Div([
                html.Img(className='uk-border-circle uk-margin', width='44', height='44',
                         src=profile.profile_picture_url, alt='profile-pic'),
                html.Div(['Administrator'], className='uk-text-small'),
                html.H3([
                    html.Span(profile.first_name, className='uk-text-bolder'),
                    html.Br(), html.Span([profile.last_name])
                ], className='uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                html.Div([profile.email], className='uk-text-small uk-margin-remove-top')
            ], className='uk-card-header'),
            html.Div([
                html.Ul([
                    html.Li([
                        html.A([
                            html.Span(**{'data-uk-icon': 'icon: mail'}, className='uk-margin-small-right'),
                            'Messages'
                        ], className='uk-flex uk-flex-middle', **{'data-uk-toggle': 'target: #messages'}),
                        html.Div([
                            html.Div([
                                html.Button(**{'data-uk-close': True}, className='uk-offcanvas-close'),
                                html.H3(['Messages']),
                                html.Div([
                                    html.Article([
                                        html.Div(**{'data-uk-icon': 'icon: mail'}),
                                        html.P([meta], className='uk-article-meta'),
                                        html.P([header], className='uk-text-bolder'),
                                        html.P([article])
                                    ], className='uk-article') for meta, header, article in messages
                                ], className='uk-flex uk-flex-wrap')
                            ], className='uk-offcanvas-bar'),
                        ], id='messages', **{'data-uk-offcanvas': 'mode: push; overlay: true'})
                    ]),
                    html.Li([
                        html.A([
                            html.Span(**{'data-uk-icon': 'icon: nut'}, className='uk-margin-small-right'),
                            'Investment'
                        ], className='uk-flex uk-flex-middle')
                    ]),
                    html.Li(className='uk-nav-divider uk-margin'),
                    html.Li('Support', className='uk-nav-header', style={'color': 'white'}),
                    html.Li([
                        html.A(['Contact Support'], **{'data-uk-toggle': 'target: #contact-support'}),
                        html.Div([
                            html.Div([
                                html.Button(**{'data-uk-close': 'true'}, className='uk-offcanvas-close'),
                                html.H3(['Contact Support']),
                                html.Div([
                                    html.Div([
                                        html.Div(**{'data-uk-icon': f'icon: {icon}; ratio: 1.8'},
                                                 className='uk-icon'),
                                        html.Div([title], className='uk-text-large uk-text-bolder'),
                                        html.Div([subtext], className='uk-text-small')
                                    ], className='uk-margin')
                                    for icon, title, subtext in [
                                        ('location', 'Location', 'Unit 17, No.30 Surprise Road, Pinetown, 3610'),
                                        ('receiver', 'Phone', '0860 258 2447'),
                                        ('mail', 'Email', 'info@bluechipinvest.co.za'),
                                        ('clock', 'Open hours', 'Mon - Sat, 08:00 - 16:00')
                                    ]], **{'data-uk-grid': 'true'},
                                    className='uk-grid-match uk-child-width-1-1 uk-margin-medium-top')
                            ], className='uk-offcanvas-bar'),
                        ], id='contact-support', **{'data-uk-offcanvas': 'mode: push; overlay: true'})
                    ]),
                    html.Li([
                        html.A(['FAQs'], **{'data-uk-toggle': 'target: #faqs'}),
                        html.Div([
                            html.Div([
                                html.Button(**{'data-uk-close': 'true'}, className='uk-offcanvas-close'),
                                html.H3(['Frequently Asked Questions'],
                                        className='uk-heading-divider uk-margin-medium-bottom'),
                                html.Div([
                                    html.Div([
                                        html.Span(**{'data-uk-icon': f'icon: question; ratio: 1.5'},
                                                  className='uk-margin-right'),
                                        html.Div([
                                            html.H3([title], className='uk-article-title'),
                                            html.P([content], className='uk-text-small')
                                        ], id=faq_id, className='uk-article-content')
                                    ], className='uk-margin-large-bottom')
                                    for title, content, faq_id in faqs
                                ], className='uk-grid uk-child-width-1-1 uk-grid-match uk-margin-medium-top',
                                    **{'data-uk-grid': 'true'})
                            ], className='uk-offcanvas-bar'),
                        ], id='faqs', **{'data-uk-offcanvas': 'mode: push; overlay: true'})
                    ]),
                    html.Li([
                        html.A(['Investment FAQs'], **{'data-uk-toggle': 'target: #investment-faqs'}),
                        html.Div([
                            html.Div([
                                html.Button(**{'data-uk-close': 'true'}, className='uk-offcanvas-close'),
                                html.H3(['Investment Frequently Asked Questions'],
                                        className='uk-heading-divider uk-margin-medium-bottom'),
                                html.Div([
                                    html.Div([
                                        html.Span(**{'data-uk-icon': f'icon: question; ratio: 1.5'},
                                                  className='uk-margin-right'),
                                        html.Div([
                                            html.H3([title], className='uk-article-title'),
                                            html.P([content], className='uk-text-small')
                                        ], id=faq_id, className='uk-article-content')
                                    ], className='uk-margin-large-bottom')
                                    for title, content, faq_id in investment_faqs
                                ], className='uk-grid uk-child-width-1-1 uk-grid-match uk-margin-medium-top',
                                    **{'data-uk-grid': 'true'})
                            ], className='uk-offcanvas-bar'),
                        ], id='investment-faqs', **{'data-uk-offcanvas': 'mode: push; overlay: true'})
                    ]),
                    html.Li([
                        html.A(['Service Status']),
                        html.Div([
                            'No reported issues. All services are functioning normally.'
                        ], **{'data-uk-drop': 'mode: click'}, className='uk-card uk-card-body uk-card-default')
                    ], className='uk-inline'),
                    sign_out_button()
                ], className='uk-nav uk-nav-default')
            ], className='uk-card-body')
        ], className='uk-card')
    ], className='uk-width-1-5@m')
