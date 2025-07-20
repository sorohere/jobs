const fs = require('fs');
const axios = require('axios');
const cheerio = require('cheerio');

// Extracts the job description from the provided job URL
async function extractJobDescription(jobUrl) {
    try {
        console.log(`Fetching job description from: ${jobUrl}`);

        const response = await axios.get(jobUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            timeout: 10000
        });

        const $ = cheerio.load(response.data);
        let jobDescription = '';

        const selectors = [
            'h2:contains("About the job")',
            'h2:contains("About the Job")',
            'h2:contains("ABOUT THE JOB")',
            '.description__text',
            '.show-more-less-html__markup',
            '[data-automation-id="jobPostingDescription"]'
        ];

        for (const selector of selectors) {
            const element = $(selector);
            if (element.length > 0) {
                if (selector.includes('About the job')) {
                    jobDescription = element.next().text().trim() ||
                                     element.parent().find('div, p').first().text().trim() ||
                                     element.siblings().first().text().trim();
                } else {
                    jobDescription = element.text().trim();
                }

                if (jobDescription && jobDescription.length > 50) {
                    break;
                }
            }
        }

        if (!jobDescription || jobDescription.length < 50) {
            const bodyText = $('body').text();
            const aboutIndex = bodyText.toLowerCase().indexOf('about the job');
            if (aboutIndex !== -1) {
                jobDescription = bodyText.substring(aboutIndex + 13, aboutIndex + 1000).trim();
            }
        }

        return jobDescription || 'Job description not found';

    } catch (error) {
        console.error(`Error fetching job description: ${error.message}`);
        return 'Error fetching job description';
    }
}

// Main function to process each job in the list
async function processJobs() {
    try {
        const jsonData = fs.readFileSync('all_jobs_huge.json', 'utf8');
        const jobs = JSON.parse(jsonData);

        console.log(`Processing ${jobs.length} jobs...\n`);

        for (let i = 0; i < jobs.length; i++) {
            const job = jobs[i];

            console.log(`Processing job ${i + 1}/${jobs.length}: ${job.position} at ${job.company}`);

            const jobDescription = await extractJobDescription(job.jobUrl);

            // Add the job_description without removing or affecting any other fields
            job.job_description = jobDescription;

            // Delay between requests
            if (i < jobs.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 2000)); // 2 sec
            }
        }

        // Save updated data
        fs.writeFileSync('alljobs_with_description.json', JSON.stringify(jobs, null, 2), 'utf8');

        console.log('\n✅ All jobs processed successfully!');
        console.log('Updated temp.json with job descriptions');

    } catch (error) {
        console.error('❌ Error processing jobs:', error);
    }
}

// Start the script
processJobs();

// 85711