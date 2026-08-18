\# YouTube TrendPulse



\### Automated YouTube Trend Detection \& Analytics Platform



YouTube TrendPulse is an automated data analytics project designed to identify emerging YouTube trends by combining real-time YouTube API data, historical performance tracking, trend-velocity analysis, engagement metrics, and interactive Power BI visualization.



Unlike a conventional trending-video dashboard, TrendPulse focuses on \*\*momentum\*\* — analyzing how quickly videos are gaining views and engagement over time to identify videos that may be emerging as significant trends.



\---



\## Overview



TrendPulse automatically collects YouTube trending videos and builds a historical record of their performance.



The system calculates:



\* View growth

\* View velocity

\* Engagement rate

\* Trend score

\* Trend status

\* Trend alerts



Videos are then classified into four categories:



| Status       | Description                                         |

| ------------ | --------------------------------------------------- |

| \*\*Emerging\*\* | High momentum and strong indicators of rapid growth |

| \*\*Growing\*\*  | Above-average momentum with increasing performance  |

| \*\*Stable\*\*   | Moderate and consistent performance                 |

| \*\*Normal\*\*   | Relatively low or limited momentum                  |



The results are presented through an interactive Power BI dashboard for monitoring and analysis.



\---



\## Key Features



\* \*\*Automated YouTube Data Collection\*\*

&#x20; Fetches the latest trending videos using the YouTube Data API.



\* \*\*Historical Performance Tracking\*\*

&#x20; Stores repeated snapshots of video performance using SQLite.



\* \*\*View Velocity Engine\*\*

&#x20; Measures how quickly videos are gaining views between collection periods.



\* \*\*Engagement Analysis\*\*

&#x20; Calculates engagement based on likes, comments, and views.



\* \*\*Trend Scoring Engine\*\*

&#x20; Combines growth, velocity, and engagement into a unified trend score.



\* \*\*Emerging Trend Detection\*\*

&#x20; Identifies videos with strong momentum relative to other monitored videos.



\* \*\*Automated Trend Alerts\*\*

&#x20; Flags videos that cross the defined emerging-trend threshold.



\* \*\*Interactive Power BI Dashboard\*\*

&#x20; Provides an analytical interface for monitoring trends and identifying high-potential videos.



\---



\## System Architecture



```text

YouTube Data API

&#x20;      │

&#x20;      ▼

Data Collection

&#x20;      │

&#x20;      ▼

Raw YouTube Data

&#x20;      │

&#x20;      ▼

Historical SQLite Storage

&#x20;      │

&#x20;      ▼

Velocity Calculation

&#x20;      │

&#x20;      ▼

Engagement Analysis

&#x20;      │

&#x20;      ▼

Trend Score Engine

&#x20;      │

&#x20;      ▼

Emerging Trend Detection

&#x20;      │

&#x20;      ▼

Processed Analytics Data

&#x20;      │

&#x20;      ▼

Power BI Dashboard

```



\---



\## Trend Scoring Methodology



TrendPulse evaluates each video using three primary signals:



\### 1. View Growth



Measures the percentage increase in views between historical observations.



\### 2. View Velocity



Measures the rate at which a video's views are increasing over time.



\### 3. Engagement Rate



Measures audience interaction using likes and comments relative to views.



The three signals are normalized and combined into a composite \*\*Emerging Trend Score\*\*.



The scoring model prioritizes velocity and growth because rapid changes in performance are stronger indicators of emerging momentum than total views alone.



\---



\## Automated Pipeline



The complete pipeline can be executed with a single command:



```bash

python src/run\_pipeline.py

```



The pipeline performs the following operations:



1\. Fetches the latest YouTube trending videos.

2\. Stores the latest snapshot in the historical database.

3\. Calculates view growth and view velocity.

4\. Calculates engagement metrics.

5\. Generates trend scores.

6\. Classifies videos into trend categories.

7\. Generates trend alerts.

8\. Produces the processed dataset used by Power BI.



Historical snapshots are retained rather than overwritten, allowing TrendPulse to analyze how video performance changes over time.



\---



\## Dashboard



The Power BI dashboard is organized into three analytical pages.



\### Page 1 — TrendPulse Overview



Provides a high-level view of the current trend landscape.



Key metrics include:



\* Live Videos

\* Emerging Trends

\* Average Trend Score

\* Average View Velocity



\### Page 2 — Trend Analysis



Provides deeper analysis of:



\* Video performance

\* Trend scores

\* View growth

\* View velocity

\* Engagement

\* Trend classifications



\### Page 3 — Emerging Trends \& Alerts



Focuses on the highest-potential videos and provides visibility into:



\* Emerging videos

\* Trend alerts

\* High-momentum content

\* Video-level trend performance



\---



\## Technology Stack



| Technology           | Purpose                                 |

| -------------------- | --------------------------------------- |

| \*\*Python\*\*           | Data collection and processing          |

| \*\*YouTube Data API\*\* | Real-time YouTube data                  |

| \*\*Pandas\*\*           | Data transformation and analysis        |

| \*\*SQLite\*\*           | Historical data storage                 |

| \*\*Power BI\*\*         | Interactive analytics and visualization |

| \*\*Git \& GitHub\*\*     | Version control and project management  |



\---



\## Project Structure



```text

YouTube-TrendPulse/

│

├── src/

│   ├── api/

│   │   ├── youtube\_client.py

│   │   └── fetch\_trending.py

│   │

│   ├── pipeline/

│   │   ├── store\_history.py

│   │   ├── calculate\_velocity.py

│   │   └── calculate\_trend\_score.py

│   │

│   └── run\_pipeline.py

│

├── data/

│   ├── raw/

│   └── processed/

│

├── requirements.txt

├── .gitignore

└── README.md

```



\---



\## Setup \& Installation



\### 1. Clone the repository



```bash

git clone <your-repository-url>

cd YouTube-TrendPulse

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



Activate the environment:



\*\*Windows\*\*



```bash

.venv\\Scripts\\activate

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Configure the YouTube API



Create an environment file:



```text

.env

```



Add your API key:



```text

YOUTUBE\_API\_KEY=your\_api\_key\_here

```



The API key should never be committed to GitHub.



\### 5. Run the pipeline



```bash

python src/run\_pipeline.py

```



\---



\## Data \& Security



API credentials are stored using environment variables and are excluded from version control.



Generated databases and pipeline outputs can also be excluded from the repository through `.gitignore`.



This keeps sensitive credentials and automatically generated data separate from the source code.



\---



\## Business Value



TrendPulse demonstrates how data analytics can be used to move from \*\*descriptive reporting to automated decision support\*\*.



Instead of only answering:



> "Which videos are trending?"



the system attempts to answer:



> \*\*"Which videos are gaining momentum and showing signs of becoming the next trend?"\*\*



This makes the project applicable to areas such as:



\* Content strategy

\* Digital marketing

\* Social media analytics

\* Audience intelligence

\* Trend monitoring

\* Creator analytics



\---



\## Future Improvements



Potential extensions include:



\* Multi-region trend monitoring

\* Automated email or notification alerts

\* Machine-learning-based trend prediction

\* Historical trend forecasting

\* Topic and keyword clustering

\* Sentiment analysis of comments

\* Automated dashboard refresh

\* Additional social-media data sources



\---



\## Author



\*\*Krishna Yadav\*\*



Data Analytics | Python | SQL | Excel | Power BI



\---



\## License



This project is intended for educational, portfolio, and demonstration purposes.



