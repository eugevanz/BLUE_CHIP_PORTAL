from datetime import datetime

import dash
from dash.html import Div, H3, Article, P, Button, Ul, Li, A, Span, Img, Nav, H2

from utils import calendar_view, sign_out_button

dash.register_page(__name__, path='/client-portal/')


def nav_offcanvas(header: str):
    return Div(
        [H3(header, className='uk-width-small uk-margin-remove')],  # Wrap in a list
        className='uk-margin-medium-bottom uk-margin-small-top uk-padding',
        style={'background-color': '#88A9C3'}
    )


def articles_offcanvas(articles: list, icon: str):
    return Div(
        [
            Article(
                Div(**{'data-uk-icon': f'icon: {icon}'}),
                P(header, className='uk-text-bolder'),
                P(article),
                className='uk-article',
                id=element
            ) for header, article, element in articles
        ],
        className='uk-flex uk-flex-wrap'
    )


def offcanvas_messages():
    return Div(
        Div(
            [
                Button(type='button', **{'data-uk-close': True}, className='uk-offcanvas-close'),
                H3('Messages'),
                Div(
                    [
                        Article(
                            [
                                Div(**{'data-uk-icon': 'icon: mail'}),
                                P(meta, className='uk-article-meta'),
                                P(header, className='uk-text-bolder'),
                                P(article)
                            ],
                            className='uk-article'
                        ) for meta, header, article in [
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
                    ],
                    className='uk-flex uk-flex-wrap'
                )
            ],
            className='uk-offcanvas-bar'
        ),
        id='messages',
        **{'data-uk-offcanvas': 'true'}
    )


def offcanvas_contact_support():
    return Div(
        Div(
            [
                Button(type='button', **{'data-uk-close': 'true'}, className='uk-offcanvas-close'),
                H3('Contact Support'),
                Div(
                    [
                        Div(
                            [
                                Div(**{'data-uk-icon': f'icon: {icon}; ratio: 1.8'}, className='uk-icon'),
                                Div(title, className='uk-text-large uk-text-bolder'),
                                Div(subtext, className='uk-text-small')
                            ],
                            className='uk-margin'
                        )
                        for icon, title, subtext in [
                        ('location', 'Location', 'Unit 17, No.30 Surprise Road, Pinetown, 3610'),
                        ('receiver', 'Phone', '0860 258 2447'),
                        ('mail', 'Email', 'info@bluechipinvest.co.za'),
                        ('clock', 'Open hours', 'Mon - Sat, 08:00 - 16:00')
                    ]
                    ],
                    **{'data-uk-grid': 'true'},
                    className='uk-grid-match uk-child-width-1-1 uk-margin-medium-top'
                )
            ],
            className='uk-offcanvas-bar'
        ),
        id='contact-support',
        **{'data-uk-offcanvas': 'true'}
    )


def offcanvas_faqs():
    return Div(
        Div(
            [
                Button(type='button', **{'data-uk-close': 'true'}, className='uk-offcanvas-close'),
                H3('Frequently Asked Questions', className='uk-heading-divider uk-margin-medium-bottom'),
                Div(
                    [
                        Div(
                            [
                                Span(**{'data-uk-icon': f'icon: question; ratio: 1.5'}, className='uk-margin-right'),
                                Div(
                                    [
                                        H3(title, className='uk-article-title'),
                                        P(content, className='uk-text-small')
                                    ],
                                    id=faq_id,
                                    className='uk-article-content'
                                )
                            ],
                            className='uk-margin-large-bottom'
                        )
                        for title, content, faq_id in [
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
                    ],
                    className='uk-grid uk-child-width-1-1 uk-grid-match uk-margin-medium-top',
                    **{'data-uk-grid': 'true'}
                )
            ],
            className='uk-offcanvas-bar'
        ),
        id='faqs',
        **{'data-uk-offcanvas': 'true'}
    )


def offcanvas_investment_faqs():
    return Div(
        Div(
            [
                Button(type='button', **{'data-uk-close': 'true'}, className='uk-offcanvas-close'),
                H3('Investment Frequently Asked Questions', className='uk-heading-divider uk-margin-medium-bottom'),
                Div(
                    [
                        Div(
                            [
                                Span(**{'data-uk-icon': f'icon: question; ratio: 1.5'}, className='uk-margin-right'),
                                Div(
                                    [
                                        H3(title, className='uk-article-title'),
                                        P(content, className='uk-text-small')
                                    ],
                                    id=faq_id,
                                    className='uk-article-content'
                                )
                            ],
                            className='uk-margin-large-bottom'
                        )
                        for title, content, faq_id in [
                        ('How do I start investing?',
                         'To start investing, you’ll need to open an investment account. Once your account is set up, you can deposit funds and choose from various investment options, such as stocks, bonds, mutual funds, or ETFs. If you’re unsure where to begin, it’s a good idea to determine your financial goals and risk tolerance before selecting investments.',
                         'start-investing'),
                        ('Can I get advice on which investments to choose?',
                         'Yes, you can receive advice on your investment options. Our team offers personalized investment recommendations based on your financial goals, risk tolerance, and time horizon. You can also schedule a consultation with an advisor for more detailed guidance.',
                         'investments-to-choose'),
                        ('How can I track my investments?',
                         'You can track your investments through your account dashboard, where you’ll find real-time updates on performance, gains, and losses. You can also set up alerts to notify you of significant changes in your portfolio or the market.',
                         'my-investments'),
                        ('What’s the difference between a conservative, balanced, and aggressive portfolio?',
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
                    ],
                    className='uk-grid uk-child-width-1-1 uk-grid-match uk-margin-medium-top',
                    **{'data-uk-grid': 'true'}
                )
            ],
            className='uk-offcanvas-bar'
        ),
        id='investment_faqs',
        **{'data-uk-offcanvas': 'true'}
    )


def menu_card():
    return Div(
        Ul(
            [
                Li('Menu', className='uk-nav-header', style={'color': 'white'}),
                Li(
                    A(
                        [Span(**{'data-uk-icon': 'icon: home'}, className='uk-margin-small-right'), 'Dashboard'],
                        className='uk-flex uk-flex-middle'
                    )
                ),
                Li(
                    A(
                        [Span(**{'data-uk-icon': 'icon: credit-card'}, className='uk-margin-small-right'),
                         'Transactions'],
                        className='uk-flex uk-flex-middle',
                        # **{'onclick': 'const element = document.getElementById("transactions"); if (element) { '
                        #               'window.scrollTo({top: element.offsetTop - 96, behavior: "smooth"}); }'}
                    )
                ),
                Li(
                    [
                        A(
                            [Span(**{'data-uk-icon': 'icon: mail'}, className='uk-margin-small-right'), 'Messages'],
                            className='uk-flex uk-flex-middle',
                            **{'data-uk-toggle': 'true'},
                            href='#messages'
                        ),
                        offcanvas_messages()
                    ]
                ),
                Li(
                    A(
                        [Span(**{'data-uk-icon': 'icon: nut'}, className='uk-margin-small-right'), 'Investment'],
                        className='uk-flex uk-flex-middle',
                        # **{'onclick': 'const element = document.getElementById("holdings"); if (element) { '
                        #               'window.scrollTo({top: element.offsetTop - 96, behavior: "smooth"}); }'}
                    )
                ),
                Li(className='uk-nav-divider uk-margin'),
                Li(
                    [
                        Div(
                            Img(className='uk-border-circle', width='44', height='44',
                                src='https://oujdrprpkkwxeavzbaow.supabase.co/storage/v1/object/public/website_images'
                                    '/jurica-koletic-7YVZYZeITc8-unsplash_3_11zon.webp',
                                alt='profile-pic'),
                            className='uk-width-auto'
                        ),
                        Div(
                            [
                                H3('Title', className='uk-card-title uk-margin-remove-bottom',
                                   style={'color': 'white'}),
                                P('April 01, 2016', className='uk-text-meta uk-margin-remove-top')
                            ],
                            className='uk-width-expand'
                        )
                    ],
                    className='uk-grid-small uk-flex-middle uk-margin-left uk-margin-top', **{'data-uk-grid': 'true'}
                ),
                Li(className='uk-nav-divider uk-margin'),
                Li('Support', className='uk-nav-header', style={'color': 'white'}),
                Li(
                    [
                        A('Contact Support', **{'data-uk-toggle': 'true'}, href='#contact-support'),
                        offcanvas_contact_support()
                    ]
                ),
                Li(
                    [
                        A('FAQs', **{'data-uk-toggle': 'true'}, href='#faqs'),
                        offcanvas_faqs()
                    ]
                ),
                Li(
                    [
                        A('Investment FAQs', **{'data-uk-toggle': 'true'}, href='#investment_faqs'),
                        offcanvas_investment_faqs()
                    ]
                ),
                Li(
                    [
                        A('Service Status'),
                        Div(
                            'No reported issues. All services are functioning normally.',
                            **{'data-uk-drop': 'mode: click'},
                            className='uk-card uk-card-body uk-card-default'
                        )
                    ],
                    className='uk-inline'
                ),
                sign_out_button()
            ],
            className='uk-nav uk-nav-default'
        ),
        className='uk-card uk-card-body uk-card-default',
        style={'background-color': '#2A3A58'}
    )


def overview_card():
    return Div([
        Div(
            Div(
                [
                    Div('Overview', className='uk-text-default uk-text-bolder'),
                    Div(datetime.now().strftime('%B %Y'), className='uk-text-small')
                ],
                className='uk-flex uk-flex-between'
            ),
            className='uk-card-header'
        ),
        Div([
            Div([
                Div([
                    Div('40', className='uk-text-large uk-text-bolder'),
                    Div('Transactions', className='uk-text-truncate', style={'font-size': '11px'})
                ]),
                Div([
                    Div('24', className='uk-text-large uk-text-bolder'),
                    Div('Income', style={'font-size': '11px'})
                ]),
                Div([
                    Div('16', className='uk-text-large uk-text-bolder'),
                    Div('Outcome', style={'font-size': '11px'})
                ])
            ], **{'data-uk-grid': 'true'}, className='uk-child-width-expand uk-text-center')
        ], className='uk-card-body'),
        Div([
            calendar_view(),
            Nav(
                Ul([
                    Li(
                        A(
                            [Span(**{'data-uk-pagination-previous': 'true'}, className='uk-margin-small-right'),
                             'September'],
                            href='#'
                        )
                    ),
                    Li(
                        A(
                            ['November', Span(**{'data-uk-pagination-next': 'true'}, className='uk-margin-small-left')],
                            href='#'
                        ),
                        className='uk-margin-auto-left'
                    )
                ], className='uk-pagination', **{'data-uk-margin': 'true'}),
                className='uk-margin-medium-top'
            ),
            A([
                Div(
                    Span(**{'data-uk-icon': 'icon: mail'}, className='uk-margin-small-right',
                         style={'color': '#89CFF0'}),
                    className='uk-width-auto'
                ),
                Div(
                    Div('Top 5 Portfolio Holdings: Tech Giants Lead with Apple, Tesla, and Amazon Driving Strong '
                        'Returns'[:80] + '...', style={'color': '#89CFF0'}, className='uk-text-bolder')
                )
            ], **{'data-uk-grid': 'true'}, **{'data-uk-toggle': 'true'}, href='#messages',
                className='uk-child-width-expand uk-grid-small uk-margin-medium-top uk-text-muted')
        ], className='uk-card-footer')
    ], className='uk-card uk-card-default uk-light', style={'background-color': '#172031'})


def portfolio_value_card():
    return Div(
        [
            Div(
                Div(
                    [
                        Div('Portfolio Value', className='uk-text-default uk-text-bolder'),
                        A(['US Dollar', Span(**{'data-uk-drop-parent-icon': True})],
                          className='uk-link-muted uk-text-small'),
                        Div(
                            [
                                Ul(
                                    [
                                        Li(A('US Dollar', className='uk-link-muted uk-text-small')),
                                        Li(A('ZA Rand', className='uk-link-muted uk-text-small')),
                                        Li(A('EURO', className='uk-link-muted uk-text-small')),
                                        Li(A('British Pound', className='uk-link-muted uk-text-small'))
                                    ],
                                    className='uk-list uk-list-divider'
                                )
                            ],
                            className='uk-card uk-card-body',
                            style={'background-color': '#2A3A58'},
                            **{'data-uk-dropdown': 'true'}
                        )
                    ],
                    className='uk-flex uk-flex-between'
                ),
                className='uk-card-header'
            ),
            Div(
                [
                    Div('Balance', className='uk-text-small'),
                    H2('R8,167,514.57',
                       className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'),
                    Div(
                        ['Compared to last month ', Span('+24.17%', className='uk-text-success')],
                        className='uk-text-small uk-margin-remove-top'
                    ),
                    Div(
                        [
                            Div(
                                Div(
                                    [
                                        Div('142M'),
                                        Div('71M', className='uk-margin-auto-vertical'),
                                        Div('0M', className='uk-flex uk-flex-column uk-flex-between uk-text-bolder',
                                            style={'font-size': '8px'})
                                    ]
                                ),
                                className='uk-width-auto'
                            )
                        ],
                        **{'data-uk-grid': 'true'},
                        className='uk-grid-divider uk-child-width-expand uk-grid-match uk-grid-small uk-margin-medium-top'
                    )
                ],
                className='uk-card-body'
            )
        ],
        className='uk-card uk-card-default uk-light',
        style={'background-color': '#172031'}
    )


def transactions():
    return Div(
        [
            Div(
                Div(
                    [
                        Div('Recent Transactions', className='uk-text-default uk-text-bolder'),
                        Div(
                            [
                                Span(**{'data-uk-icon': 'icon: table'}),
                                Span('Filter', className='uk-margin-small-left')
                            ],
                            className='uk-text-small uk-flex uk-flex-middle'
                        )
                    ],
                    className='uk-flex uk-flex-between'
                ),
                className='uk-card-header'
            ),
            # Div(
            #     Table(
            #         Thead(
            #             Tr(
            #                 [
            #                     Th('Type'),
            #                     Th('Amount'),
            #                     Th('Method')
            #                 ]
            #             )
            #         ),
            #         Tbody(
            #             [
            #                 Tr([
            #                     Td(
            #                         [
            #                             Span(
            #                                 **{
            #                                     'data-uk-icon': f'icon: {"plus-circle" if tx_type[0] == "Received" else "minus-circle"}; ratio: 1.5'
            #                                 },
            #                                 className=f'uk-text-{"success" if tx_type[0] == "Received" else "danger"}'
            #                             ),
            #                             Div([
            #                                 Div(title, className='uk-text-bolder'),
            #                                 Div(f'{tx_type[0]} • {tx_type[1]}', className='uk-text-small')
            #                             ], className='uk-margin-small-left')
            #                         ],
            #                         className='uk-flex uk-flex-middle'
            #                     ),
            #                     Td([
            #                         Div(f'R {amount[0]}', className='uk-text-bolder'),
            #                         Div(f'R {amount[1]}', className='uk-text-small')
            #                     ]),
            #                     Td([
            #                         Div(method[0], className='uk-text-bolder'),
            #                         Div(method[1], className='uk-text-small')
            #                     ])
            #                 ]) for title, tx_type, amount, method in [
            #                 ('Company', ('Sent', 'Aug 24 2024'), (1500.00, 1371.81), ('Credit Card', '**** 3560')),
            #                 (
            #                     'Revenue', ('Received', 'Aug 24 2024'), (1500.00, 1371.81),
            #                     ('Bank Transfer', '**** 3560')),
            #                 ('Bonus', ('Received', 'Aug 24 2024'), (1500.00, 1371.81), ('Credit Card', '**** 3560')),
            #                 ('Dog food', ('Sent', 'Aug 24 2024'), (1500.00, 1371.81), ('Bank Transfer', '**** 3560')),
            #                 ('Company', ('Sent', 'Aug 24 2024'), (1500.00, 1371.81), ('Bank Transfer', '**** 3560'))
            #             ]
            #             ]
            #         ),
            #         className='uk-table uk-table-divider'
            #     ),
            #     className='uk-card-body'
            # ),
            Div(
                Nav(
                    Ul(
                        [
                            Li(
                                A([
                                    Span(**{'data-uk-pagination-previous': True}, className='uk-margin-small-right'),
                                    'Previous'
                                ], href='#')
                            ),
                            Li(
                                A([
                                    'Next',
                                    Span(**{'data-uk-pagination-next': True}, className='uk-margin-small-left')
                                ], href='#'),
                                className='uk-margin-auto-left'
                            )
                        ],
                        className='uk-pagination',
                        **{'data-uk-margin': 'true'}
                    )
                ),
                className='uk-card-footer'
            )
        ],
        className='uk-card uk-card-default uk-light',
        style={'background-color': '#172031'},
        id='transactions'
    )


def holdings():
    return Div(
        [
            Div(
                Div(
                    Div('Holdings', className='uk-text-default uk-text-bolder'),
                    className='uk-flex uk-flex-between'
                ),
                className='uk-card-header'
            ),
            Div([
                Div(
                    [
                        Div(
                            [
                                Div('Stocks (Equities)', className='uk-text-small'),
                                H2(
                                    'R8,167,514.57',
                                    className='uk-text-bolder uk-margin-remove-top uk-margin-remove-bottom uk-text-truncate'
                                ),
                                Div(
                                    [
                                        'Compared to last month ',
                                        Span('+24.17%', className='uk-text-success')
                                    ],
                                    className='uk-text-small uk-margin-remove-top'
                                )
                            ]
                        ),
                        Button(
                            'View All',
                            style={'background-color': '#88A9C3', 'color': '#091235'},
                            className='uk-button uk-button-small'
                        )
                    ],
                    className='uk-flex uk-flex-between uk-flex-middle'
                ),
                P(
                    'Apple Inc. (AAPL) is a multinational technology company based in Cupertino, California, best known for its '
                    'innovative hardware, software, and digital services. Listed on the NASDAQ stock exchange under the ticker '
                    'symbol AAPL, Apple is one of the most valuable companies in the world, consistently maintaining its '
                    'position as a leader in the tech industry.',
                    className='uk-text-small'
                )
            ], className='uk-card-body'),
            Div(
                Nav(
                    Ul(
                        [
                            Li(
                                A(
                                    Span(**{'data-uk-pagination-previous': True}, className='uk-margin-small-right'),
                                    'Bonds (Fixed Income Securities)',
                                    href='#'
                                )
                            ),
                            Li(
                                A(
                                    [
                                        'Real Estate',
                                        Span(**{'data-uk-pagination-next': True}, className='uk-margin-small-left')
                                    ],
                                    href='#'
                                ),
                                className='uk-margin-auto-left'
                            )
                        ],
                        className='uk-pagination',
                        **{'data-uk-margin': 'true'}
                    )
                ),
                className='uk-card-footer'
            )
        ],
        className='uk-card uk-card-default uk-light',
        style={'background-color': '#172031'},
        id='holdings'
    )


def layout():
    return Div(
        Div(
            Div(
                [
                    Div(menu_card(), className='uk-width-1-3@m'),
                    Div(overview_card(), className='uk-width-1-3@m'),
                    Div(portfolio_value_card(), className='uk-width-1-3@m'),
                    # Div(assets_card()),  # Uncomment when ready to use
                    Div(transactions(), className='uk-width-1-2@m'),
                    Div(holdings(), className='uk-width-1-2@m')
                ],
                **{'data-uk-grid': 'true'},
                className='uk-child-width-1-4@m uk-grid-small uk-grid-match uk-flex-right',
                style={'padding-top': '16px'}
            ),
            className='uk-container'
        ),
        style={'background-color': '#091235'}
    )
