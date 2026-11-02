/* Contract tests for the stand-alone, synthetic CFB Survivor Showcase engine.
   Run: node tests/cfb_survivor.test.cjs
   No network, no paid provider calls, no private ABIQ imports. */
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");

const root=path.join(__dirname,"..");
const source=fs.readFileSync(path.join(root,"frontend","cfb_survivor.js"),"utf8")
  .split("// Add the new page")[0];
assert(source.includes("function cfbOptimize("),"The scenario engine must remain testable");
const context=vm.createContext({});
vm.runInContext(source+`
  globalThis.testApi={teams:CFB_DEMO_TEAMS,fixtures:CFB_FIXTURES,optimize:cfbOptimize};
`,context,{timeout:10000});
const {teams,fixtures,optimize}=context.testApi;

for(const conference of ["SEC","BIG TEN"]){
  const fixture=fixtures[conference];
  const expectedTeams=conference==="SEC"?16:18;
  assert.equal(fixture.names.length,expectedTeams);
  const base=optimize(conference);
  assert.equal(base.error,undefined);
  assert.equal(Object.keys(base.path).length,14);
  assert.equal(new Set(Object.values(base.path)).size,14);
  for(const [team,rows] of Object.entries(fixture.byTeam)){
    assert.equal(rows.length,14);
    assert.equal(rows.filter(Boolean).length,12,`${conference} ${team}: requires exactly two illustrated byes`);
    assert.equal(new Set(rows.filter(Boolean).map(row=>row.opponent)).size,12);
    rows.forEach((row,i)=>{
      if(!row)return;
      const reverse=fixture.byTeam[row.opponent][i];
      assert.equal(reverse.opponent,team);
      assert(Math.abs(row.probability+reverse.probability-1)<1e-9);
      assert(row.probability>0 && row.probability<1);
    });
  }
  for(const [week,team] of Object.entries(base.path)){
    assert(fixture.byTeam[team][Number(week)-1],`Missing chosen Week ${week} game`);
  }
  const duplicate=optimize(conference,{1:base.path[1],2:base.path[1]});
  assert(duplicate.error,"Team reuse across weeks must be rejected");

  let changedAny=false;
  const alternatives=fixture.names.filter(team=>team!==base.path[1] && fixture.byTeam[team][0]);
  for(const alternate of alternatives){
    const plan=optimize(conference,{1:alternate});
    if(plan.error) continue;
    assert.equal(plan.path[1],alternate);
    assert.equal(new Set(Object.values(plan.path)).size,14);
    if(Object.keys(base.path).some(w=>Number(w)>1 && base.path[w]!==plan.path[w])) changedAny=true;
  }
  assert(changedAny,`${conference} should demonstrate a downstream scenario change`);

  // Lock a later week while preserving the first seven already-planned picks.
  const preserve=Object.fromEntries(Array.from({length:7},(_,i)=>[i+1,base.path[i+1]]));
  const week8Choices=fixture.names.filter(team=>fixture.byTeam[team][7] && !Object.values(preserve).includes(team));
  const candidate=week8Choices.find(team=>!optimize(conference,{...preserve,8:team}).error);
  assert(candidate,`Must have an eligible Week 8 scenario in ${conference}`);
  const replanned=optimize(conference,{...preserve,8:candidate});
  for(let w=1;w<8;w++) assert.equal(replanned.path[w],base.path[w]);
  assert.equal(replanned.path[8],candidate);
  console.log(`${conference}: valid 14-week plans, full illustrated schedules, no repeats, dynamic downstream changes`);
}
console.log("CFB Survivor Showcase engine tests passed.");
