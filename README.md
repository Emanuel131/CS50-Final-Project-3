<a href='https://secure-island-71749.herokuapp.com'>
    <img src='./media/logo.png' alt='HSE SMASH Logo' title='HSE SMASH' align='right' height='60'/>
</a>

# HSE SMASH (CS50 Final Project)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
![GitHub last commit](https://img.shields.io/github/last-commit/Snowfighter/CS50-Final-Project)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

:star: Star me on GitHub — just for fun and motivation :grinning:

[HSE SMASH](https://secure-island-71749.herokuapp.com) is my final project for Harvard CS50 online course. It is a web app that allows you to compare girls by there profile photos & find the hottest one :fire: :fire: :fire: :fire: :smirk: :smirk: :smirk: :smirk:

<a href='https://secure-island-71749.herokuapp.com'>
    <img src='./media/front_page.png' alt='Front Page'/>
</a>

## Table of contents

-   [Idea](#idea)
-   [Structure](#structure)
    -   [Database](#phpLiteAdmin)
    -   [VK](#vk)
    -   [Application](#application.py)

## Idea

The idea of making such an app came to me after watching ["The Social Network"](https://www.imdb.com/title/tt1285016/) movie. Where Mark Zuckerberg gets pissed off by his ex girlfriend and, being a little bit drunk, creates FaceSmash, a web-app that allows to compare Harvard girls between each other, two at a time. 

I was not pissed by my ex, nor was I drunk, but decided to reimplement this app using Python as a backend language for my Flask Server and JS/HTML/CSS for my pages. Being a HSE student I have decided to use VK society for getting the profile pages of the girls from my university. 

Below I give a detailed description of all the project, so feel free to use it as a template for making such a prank in your own university :wink:

## Structure
```
├── phpLiteAdmin
│   └── HSE.db
├── VK
│   └── vk_export.py

├── application.py
├── member.py
├── templates
│   └── credits.html
│   └── hottest.html
│   └── index.html
│   └── layout.html
│   └── personal.html
├── static
│   ├── fonts
│   │   └── SexyShoutFreeFont.ttf
│   │   └── SexyShoutFreeFont.otf
│   └── Jobs.jpg
│   └── Jobs2.jpg
│   └── Slushi.jpg
│   └── scripts.js
│   └── styles.css
├── LICENSE
├── README.md

```

### phpLiteAdmin
Before writing my web app I need a database with my girls. For that I need to decide what tools to use and what fields to create for each member. 

I have decided to use [SQLite](https://www.sqlite.org/index.html) for this project and [phpLiteAdmin](https://www.phpliteadmin.org) for local management and testing. The latter was utilized for initial cretion of the db, table and fields, though it could be done programmatically in Python. Here is the link for how to start a local phpLiteAdmin server "https://bitbucket.org/phpliteadmin/public/wiki/NoWebserver". 

The snipet of resulting "members" table: 

	| tab_id | vk_id | first_name |	last_name	    | sex | photo_link	                                                                                | rating |
    | ------ | ----- | ---------- | --------------- | --- | ------------------------------------------------------------------------------------------- | --- |
	| 	2	 | 270	 | Irina	  |   Rybakova	    | 1	  | https://pp.userapi.com/c629116/v629116270/14349/NivavpUia9k.jpg?ava=1	                    | 2.0 |
	| 	5	 | 509	 | Alyona	  |   Vershinina	| 1	  | https://pp.userapi.com/c852128/v852128160/2b6c0/pnVQlSodoEE.jpg?ava=1	                    | 0.0 |
	| 	7	 | 605	 | Lena	      |   Udodova	    | 1	  | https://sun1-11.userapi.com/kDDxts6O4jouBIScMt4iH7nRVT_JKxzKkv9gaw/_IWoF3dFzlA.jpg?ava=1	| 0.0 |
	| 	8	 | 680	 | Katya	  |   Semenko	    | 1	  | https://pp.userapi.com/c627316/v627316680/43095/ZVEhuFxe59Y.jpg?ava=1	                    | 0.0 |
	| 	9	 | 692	 | Liza	      |   Kulik	        | 1	  | https://pp.userapi.com/c630416/v630416692/7446/Rbatb84-q9k.jpg?ava=1	                    | 0.0 |
	| 	13	 | 796	 | Alina	  |   Sazonova	    | 1	  | https://pp.userapi.com/c638923/v638923796/4ebfc/Pa1bYmNPZgE.jpg?ava=1	                    | 0.0 |
	| 	16	 | 896	 | Olga	      |   Borodulina	| 1	  | https://pp.userapi.com/c313/u00896/a_2f90c1d9.jpg?ava=1	                                    | 0.0 |
	| 	17	 | 905	 | Alina	  |   Yashina	    | 1	  | https://pp.userapi.com/c824504/v824504324/1a43e4/x0DNcr_UhG0.jpg?ava=1	                    | 0.0 |
	| 	19	 | 982	 | Natalia	  |   Koryakovtseva	| 1	  | https://pp.userapi.com/c622820/v622820982/3a9a4/pHC7A_lkhls.jpg?ava=1	                    | 0.0 |
	| 	21	 | 1066	 | Alina	  |   Kirnos	    | 1	  | https://pp.userapi.com/c625431/v625431066/15bbc/OKAT3H0lZVs.jpg?ava=1	                    | 0.0 |
	| 	23	 | 1360	 | Dinara	  |   Izmaylova	    | 1	  | https://pp.userapi.com/c9984/u01360/a_0dcbc0a1.jpg?ava=1	                                | 0.0 |
	| 	25	 | 1422	 | Masha	  |   Egorova	    | 1	  | https://pp.userapi.com/c10566/u01422/a_09cc6b8c.jpg?ava=1	                                | 0.0 |
	| 	30	 | 2928	 | Polina	  |   Dolgova	    | 1	  | https://sun1-2.userapi.com/922oInynbOfu9uHPjN4pgLqvTnYThQ5FhubABA/kFhlyKTN8Mg.jpg?ava=1	    | 0.0 |
	| 	31	 | 3212	 | Olga	      |   Kornaukhova	| 1	  | https://pp.userapi.com/c9322/u03212/a_d2c6104c.jpg?ava=1	                                | 0.0 |
	| 	32	 | 3233	 | Irina	  |   Lobuzova	    | 1	  | https://pp.userapi.com/c9359/u03233/a_d7bff568.jpg?ava=1	                                | 0.0 |
	| 	33	 | 3264	 | Elena	  |   Lebedinskaya	| 1	  | https://pp.userapi.com/c638429/v638429264/3342d/wIMoK_pBxdE.jpg?ava=1	                    | 0.0 |
	| 	35	 | 3807	 | Karina	  |   Afonskaya	    | 1	  | https://pp.userapi.com/c637419/v637419653/5fa99/urx9eBmH4tM.jpg?ava=1	                    | 0.0 |
	| 	36	 | 3950	 | Tatyana	  |   Pashaeva	    | 1	  | https://pp.userapi.com/c637823/v637823950/55f05/7-MsFOpNqEg.jpg?ava=1	                    | 0.0 |
	| 	38	 | 4223	 | Anna	      |   Shklyaeva	    | 1	  | https://pp.userapi.com/c636119/v636119223/18e9d/nRai9GVi348.jpg?ava=1	                    | 0.0 |
	| 	42	 | 4986	 | Yulia	  |   Sannikova	    | 1	  | https://pp.userapi.com/c834200/v834200492/6ad1c/8kFYLvowp98.jpg?ava=1	                    | 0.0 |
	| 	43	 | 5323	 | Alexandra  |	Kriventsova	    | 1	  | https://pp.userapi.com/c844417/v844417151/a85f9/nZJ1rxD8HzU.jpg?ava=1	                    | 0.0 |
	| 	44	 | 5344	 | Yulenka	  |   Markova	    | 1	  | https://sun1-16.userapi.com/f75DUNhVCcRuHen59C6y179l2CoZlTgn9zH5SA/MCRC6q1_CMA.jpg?ava=1	| 0.0 |
	| 	45	 | 5530	 | Ekaterina  |	Matrosova	    | 1	  | https://pp.userapi.com/c841638/v841638562/72497/zp8BVlx7nwU.jpg?ava=1	                    | 0.0 |
	| 	46	 | 5757	 | Yulia	  |   Monakhova	    | 1	  | https://pp.userapi.com/c630318/v630318757/38d52/HRH3f175FGQ.jpg?ava=1	                    | 0.0 |
	| 	48	 | 5863	 | Rita	      |   Podkhalyuzina	| 1	  | https://pp.userapi.com/c846018/v846018569/c2894/vVY7yWjxkpM.jpg?ava=1	                    | 0.0 |
	| 	49	 | 5948	 | Katerina	  |   Mordovina	    | 1	  | https://pp.userapi.com/c604627/v604627948/24e92/vq9_oTpvMfE.jpg?ava=1	                    | 0.0 |
	| 	50	 | 6082	 | Lena	      |   Kropotova	    | 1	  | https://pp.userapi.com/c845524/v845524805/12c3e5/3qetDzlo9EE.jpg?ava=1	                    | 0.0 |
	| 	52	 | 6244	 | Tatyana	  |   Tarasova	    | 1	  | https://sun1-20.userapi.com/c831508/v831508925/15ace9/CG0Gq1MC9_s.jpg?ava=1	                | 0.0 |
	| 	53	 | 6616	 | Elena	  |   Ustinova	    | 1	  | https://pp.userapi.com/c840129/v840129678/6d8cc/g54CSnZ1v5M.jpg?ava=1	                    | 0.0 |
	| 	58	 | 6998	 | Irina	  |   Lesovskaya	| 1	  | https://pp.userapi.com/c1035/u06998/a_ab0d0a78.jpg?ava=1	                                | 0.0 |

### VK

### application.py

