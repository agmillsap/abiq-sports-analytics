/* Standalone contract: dashboard cannot fabricate later NFL picks or
   reinterpret synthetic CFB inputs as validated ABIQ probabilities. */
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");
const root=path.join(__dirname,"..");
const cfb=fs.readFileSync(path.join(root,"frontend","cfb_survivor.js"),"utf8");
const weekly=fs.readFileSync(path.join(root,"frontend","weekly_showcase.js"),"utf8");
const html=fs.readFileSync(path.join(root,"frontend","showcase_exec.html"),"utf8");
const py=fs.readFileSync(path.join(root,"showcase_v3.py"),"utf8");
const context=vm.createContext({});
vm.runInContext(cfb.split("// Add the new page")[0]+"\n"+
  weekly.split("// DOM integration")[0]+"\n"+
  "globalThis.testApi={rows:abiqWeeklyRows,logos:CFB_TEAM_LOGO_IDS,teams:CFB_DEMO_TEAMS,scenarios:cfbScenario,override:cfbOverride,state:CFB_DEMO_STATE,fixtures:CFB_FIXTURES};",
  context,{timeout:10000});
const api=context.testApi;
const data={recommendations:[
  {team:"LAC",opponent:"ARI",probability:"81.1%",confidence:"High"},
  {team:"JAX",opponent:"CLE",probability:"75.8%",confidence:"High"},
  {team:"DET",opponent:"NO",probability:"71.7%",confidence:"High"},
  {team:"PHI",opponent:"WAS",probability:"65.0%",confidence:"Medium"}
]};
const first=api.rows(1,data);
assert.equal(first.length,5);
assert.equal(first.filter(row=>row.sport==="NFL").length,3);
assert.equal(first.filter(row=>row.sport==="CFB").length,2);
assert(first.filter(row=>row.sport==="NFL").every(row=>row.illustrative===false));
assert(first.filter(row=>row.sport==="CFB").every(row=>row.illustrative===true));
for(let week=2;week<=14;week++){
  const rows=api.rows(week,data);
  assert.equal(rows.length,2);
  assert(rows.every(row=>row.sport==="CFB"),"Cannot manufacture NFL Week "+week+" forecasts");
  for(const row of rows){
    const scenario=api.scenarios(row.conference);
    assert.equal(row.team,scenario.path[week]);
    assert.equal(row.opponent,api.fixtures[row.conference].byTeam[row.team][week-1].opponent);
  }
}
const allTeams=Object.values(api.teams).flat().map(row=>row[0]);
assert.equal(allTeams.length,34);
assert.equal(Object.keys(api.logos).length,34);
assert(allTeams.every(name=>Number.isInteger(api.logos[name])),"Each CFB team needs a CDN logo ID");
const original=first.find(row=>row.conference==="SEC").team;
api.state.conference="SEC";
const alternate=api.fixtures.SEC.names.find(team=>team!==original &&
  api.fixtures.SEC.byTeam[team][0] && !api.fixtures.SEC.byTeam[team][0].error);
assert(alternate);
assert.equal(api.override(1,alternate),true);
assert.equal(api.rows(1,data).find(row=>row.conference==="SEC").team,alternate);
assert.equal(api.rows(1,data).find(row=>row.conference==="BIG TEN").team,
  first.find(row=>row.conference==="BIG TEN").team);
for(const id of ["abiq-weekly-command","abiq-weekly-week","abiq-weekly-nfl-picks","abiq-weekly-cfb-picks"])
  assert(html.includes('id="'+id+'"'));
assert(html.includes("<h2>NFL Forecasts</h2>"));
assert(weekly.includes('nav.textContent="NFL Forecasts"'));
assert(py.includes('name="abiq_public_showcase_v13"'));
assert(py.includes('weekly_showcase.js'));
assert(py.includes('weekly_showcase.css'));
console.log("Mixed weekly dashboard, CFB branding and no fabricated NFL forecasts: PASS");
