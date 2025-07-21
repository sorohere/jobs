const fs = require('fs-extra');
const linkedIn = require('linkedin-jobs-api');
const pLimit = require('p-limit').default; 

// Semiconductor keywords based on case study skill areas
const keywords = [
  "VLSI Design Engineer", "RTL Design Engineer", "ASIC Engineer", "SoC Engineer",
  "Digital Design Engineer", "Analog Design Engineer", "FPGA Engineer",
  "DFT Engineer", "EDA Engineer", "Test Engineer",
  "AI Hardware Engineer", "ML Chip Engineer", "Embedded Systems Engineer",
  "Semiconductor Process Engineer", "Quantum Computing Engineer"
];

// Key hiring locations in India
const locations = ["Bangalore", "Hyderabad", "Pune", "Chennai", "Noida", "Gurgaon"];

// Roles focused on fresher/early-career talent
const experienceLevels = ["entry level", "associate"];

// Work mode filters
const remoteOptions = ["on-site", "remote", "hybrid"];

const jobType = "full time";
const dateSincePosted = "past Week";
const salary = "100000";
const limit = 10; // Recommended to avoid throttling
const outDir = "data";
const CONCURRENCY_LIMIT = 4; // You can bump this to ~6–8 based on network stability
const limitConcurrency = pLimit(CONCURRENCY_LIMIT);

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// === MAIN QUERY FUNCTION ===
async function fetchJobs({ keyword, location, experienceLevel, remoteFilter }) {
  const safeKeyword = keyword.replace(/\s+/g, '_');
  const fileName = `${outDir}/${safeKeyword}_${location}_${remoteFilter}.json`;

  const options = {
    keyword,
    location,
    dateSincePosted,
    jobType,
    salary,
    experienceLevel,
    remoteFilter,
    limit,
    page: "0"
  };

  try {
    console.log(`🔎 ${keyword} | ${location} | ${remoteFilter} | ${experienceLevel}`);
    const jobs = await linkedIn.query(options);

    if (jobs && jobs.length > 0) {
      const enriched = jobs.map(job => ({
        ...job,
        metadata: { keyword, location, experienceLevel, remoteFilter }
      }));
      await fs.outputJson(fileName, enriched, { spaces: 2 });
      console.log(`✅ Saved ${jobs.length} jobs → ${fileName}`);
    } else {
      console.log(`⚠️ No jobs for ${keyword} in ${location} (${remoteFilter})`);
    }

    await sleep(600); // brief delay to reduce throttling
  } catch (err) {
    console.error(`❌ Error: ${keyword} | ${location} | ${remoteFilter} → ${err.message}`);
  }
}

// === BUILD AND EXECUTE ALL COMBINATIONS ===
(async () => {
  console.time("⏱️ Job scraping duration");
  const tasks = [];

  for (const keyword of keywords) {
    for (const location of locations) {
      for (const experienceLevel of experienceLevels) {
        for (const remoteFilter of remoteOptions) {
          tasks.push(limitConcurrency(() =>
            fetchJobs({ keyword, location, experienceLevel, remoteFilter })
          ));
        }
      }
    }
  }

  console.log(`🚀 Starting ${tasks.length} job queries...`);

  const results = await Promise.allSettled(tasks);
  const successful = results.filter(r => r.status === "fulfilled").length;
  const failed = results.length - successful;

  console.log(`✅ Completed scraping. Success: ${successful}, Failed: ${failed}`);
  console.timeEnd("⏱️ Job scraping duration");
})();
