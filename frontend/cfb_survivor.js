/* Public CFB Survivor Showcase.
   All schedules and probabilities are synthetic, deterministic demonstration inputs.
   This does not import private ABIQ code, CFB production picks, or paid data.
   The scenario engine solves a constrained season-long assignment: one team per
   week, no team reuse, maximize the product of illustrative win probabilities. */
const CFB_DEMO_TEAMS = {
  SEC: [
    ["Alabama",1.70],["Arkansas",.65],["Auburn",.95],["Florida",1.02],
    ["Georgia",1.83],["Kentucky",.85],["LSU",1.49],["Mississippi State",.55],
    ["Missouri",1.08],["Oklahoma",1.25],["Ole Miss",1.45],["South Carolina",1.30],
    ["Tennessee",1.42],["Texas",1.76],["Texas A&M",1.32],["Vanderbilt",.47]
  ],
  "BIG TEN": [
    ["Illinois",.97],["Indiana",1.31],["Iowa",1.13],["Maryland",.57],
    ["Michigan",1.57],["Michigan State",.78],["Minnesota",.84],["Nebraska",.96],
    ["Northwestern",.43],["Ohio State",1.84],["Oregon",1.73],["Penn State",1.57],
    ["Purdue",.39],["Rutgers",.59],["UCLA",1.14],["USC",1.36],
    ["Washington",1.14],["Wisconsin",1.03]
  ]
};
const CFB_WEEKS = 14;
const CFB_DEMO_STATE = {conference:"SEC", byConference:{}};

function cfbHash(input) {
  let value = 2166136261;
  for (const letter of input) {
    value ^= letter.charCodeAt(0);
    value = Math.imul(value, 16777619);
  }
  return value >>> 0;
}

function cfbGameKey(a,b) {
  return [a,b].sort().join("|");
}

function cfbPairActiveTeams(active, alreadyPlayed, week) {
  // Backtracking makes each synthetic matchup symmetric and avoids repeat opponents.
  const ordered = [...active].sort((a,b) =>
    cfbHash(a + ":" + week) - cfbHash(b + ":" + week)
  );
  function solve(remaining) {
    if (!remaining.length) return [];
    const first = remaining[0];
    const options = remaining.slice(1)
      .filter(other => !alreadyPlayed.has(cfbGameKey(first,other)))
      .sort((a,b) => cfbHash(first + a + week) - cfbHash(first + b + week));
    for (const second of options) {
      const rest = remaining.slice(1).filter(team => team !== second);
      const downstream = solve(rest);
      if (downstream) return [[first,second],...downstream];
    }
    return null;
  }
  return solve(ordered);
}

function cfbFixture(conference) {
  const teams = CFB_DEMO_TEAMS[conference];
  const strengths = Object.fromEntries(teams);
  const names = teams.map(row => row[0]);
  const byTeam = Object.fromEntries(names.map(name => [name,Array(CFB_WEEKS).fill(null)]));
  const previouslyPlayed = new Set();
  const groupSize = conference === "SEC" ? 4 : 6;
  const groups = conference === "SEC" ? 4 : 3;
  for (let week = 1; week <= CFB_WEEKS; week++) {
    const active = names.filter((team,index) => {
      const group = Math.floor(index / groupSize);
      return week !== 3 + group && week !== 10 + group;
    });
    const pairs = cfbPairActiveTeams(active,previouslyPlayed,week);
    if (!pairs || pairs.length * 2 !== active.length) {
      throw new Error("Illustrative CFB schedule could not be paired for " + conference + " Week " + week);
    }
    for (const [a,b] of pairs) {
      const home = cfbHash(a + ":" + b + ":" + week) % 2 === 0 ? a : b;
      const away = home === a ? b : a;
      const homeProbability = Math.max(.13,Math.min(.87,
        1 / (1 + Math.exp(-((strengths[home]-strengths[away])*1.58 + .17)))
      ));
      byTeam[home][week-1] = {week,team:home,opponent:away,home:true,probability:homeProbability};
      byTeam[away][week-1] = {week,team:away,opponent:home,home:false,probability:1-homeProbability};
      previouslyPlayed.add(cfbGameKey(a,b));
    }
  }
  return {names,byTeam};
}

const CFB_FIXTURES = Object.fromEntries(
  Object.keys(CFB_DEMO_TEAMS).map(conference => [conference,cfbFixture(conference)])
);

// Rectangular Hungarian algorithm, O(weeks * teams^2).
// Costs are -log(p), so minimizing their sum maximizes all-week survival
// under an explicitly illustrative independent-game objective.
function cfbHungarian(cost) {
  const n = cost.length;
  if (!n) return [];
  const m = cost[0].length;
  if (m < n) return null;
  const u = Array(n+1).fill(0), v = Array(m+1).fill(0);
  const p = Array(m+1).fill(0), way = Array(m+1).fill(0);
  for (let i=1;i<=n;i++) {
    p[0]=i;
    let j0=0;
    const minv=Array(m+1).fill(Infinity), used=Array(m+1).fill(false);
    do {
      used[j0]=true;
      const i0=p[j0];
      let delta=Infinity,j1=0;
      for (let j=1;j<=m;j++) if (!used[j]) {
        const cur=cost[i0-1][j-1]-u[i0]-v[j];
        if (cur<minv[j]) {minv[j]=cur;way[j]=j0;}
        if (minv[j]<delta) {delta=minv[j];j1=j;}
      }
      if (!Number.isFinite(delta) || j1===0) return null;
      for (let j=0;j<=m;j++) {
        if (used[j]) {u[p[j]]+=delta;v[j]-=delta;}
        else {minv[j]-=delta;}
      }
      j0=j1;
    } while(p[j0]!==0);
    do {
      const j1=way[j0];
      p[j0]=p[j1];
      j0=j1;
    } while(j0!==0);
  }
  const result=Array(n).fill(-1);
  for(let j=1;j<=m;j++) if(p[j]>0) result[p[j]-1]=j-1;
  return result;
}

function cfbOptimize(conference, fixed={}) {
  const fixture=CFB_FIXTURES[conference], used=new Set(), path={};
  for (const [weekText,team] of Object.entries(fixed)) {
    const week=Number(weekText);
    if (!Number.isInteger(week) || week<1 || week>CFB_WEEKS ||
        !fixture.byTeam[team]?.[week-1]) {
      return {error:"That selection is not available in the illustrative Week " + week + " schedule."};
    }
    if (used.has(team)) return {error:team+" is already reserved for another week. A team can only be used once."};
    used.add(team);
    path[week]=team;
  }
  const remainingWeeks=Array.from({length:CFB_WEEKS},(_,i)=>i+1).filter(w=>!path[w]);
  const teams=fixture.names.filter(team=>!used.has(team));
  const impossible=1000000;
  const cost=remainingWeeks.map(w=>teams.map(team => {
    const option=fixture.byTeam[team][w-1];
    return option ? -Math.log(option.probability) : impossible;
  }));
  const matches=cfbHungarian(cost);
  if (!matches || matches.some((col,i)=>col<0 || cost[i][col]>=impossible)) {
    return {error:"No complete season path fits these choices. Try a different pick or reset."};
  }
  remainingWeeks.forEach((week,index)=>{path[week]=teams[matches[index]];});
  if (new Set(Object.values(path)).size!==CFB_WEEKS) {
    return {error:"The illustrative plan violated the no-reuse rule."};
  }
  const probabilities=Object.keys(path).map(week=>fixture.byTeam[path[week]][Number(week)-1].probability);
  return {path,average:probabilities.reduce((a,b)=>a+b,0)/probabilities.length};
}

function cfbScenario(conference) {
  if (!CFB_DEMO_STATE.byConference[conference]) {
    const plan=cfbOptimize(conference);
    if (plan.error) throw new Error(plan.error);
    CFB_DEMO_STATE.byConference[conference] = {
      locks:{}, path:plan.path, average:plan.average, week:1,
      team:plan.path[1], changes:[], message:""
    };
  }
  return CFB_DEMO_STATE.byConference[conference];
}

function cfbPercent(probability) {
  return (100*probability).toFixed(1)+"%";
}

function cfbNode(tag,className,text) {
  const element=document.createElement(tag);
  if(className) element.className=className;
  if(text!==undefined) element.textContent=String(text);
  return element;
}

function cfbOption(week,team) {
  return CFB_FIXTURES[CFB_DEMO_STATE.conference].byTeam[team]?.[week-1] ?? null;
}

function cfbOverride(week,team) {
  const s=cfbScenario(CFB_DEMO_STATE.conference);
  const previous={...s.path};
  const fixed={...s.locks};
  // A change in a later week should never silently rewrite earlier choices.
  for(let w=1;w<week;w++) fixed[w]=previous[w];
  fixed[week]=team;
  const plan=cfbOptimize(CFB_DEMO_STATE.conference,fixed);
  if(plan.error) {s.message=plan.error;return false;}
  s.locks[week]=team;
  s.path=plan.path;
  s.average=plan.average;
  s.week=week;
  s.team=team;
  s.changes=Array.from({length:CFB_WEEKS-week},(_,i)=>week+i+1)
    .filter(w=>previous[w]!==plan.path[w])
    .map(w=>({week:w,before:previous[w],after:plan.path[w]}));
  s.message=s.changes.length
    ? "Selection locked. "+s.changes.length+" future "+(s.changes.length===1?"week was":"weeks were")+" reoptimized."
    : "Selection locked. The remaining optimal path did not need to change.";
  return true;
}

function cfbMetric(label,value,sub) {
  const el=cfbNode("article","abiq-cfb-metric abiq-surface");
  el.append(cfbNode("span","",label),cfbNode("strong","",value),cfbNode("small","",sub));
  return el;
}

function cfbRender(parentElement) {
  const conference=CFB_DEMO_STATE.conference;
  const fixture=CFB_FIXTURES[conference], s=cfbScenario(conference);
  const area=parentElement.querySelector("#page-cfb-survivor");
  if(!area) return;
  for (const btn of area.querySelectorAll("[data-conference]")) {
    btn.setAttribute("aria-pressed",String(btn.dataset.conference===conference));
    btn.onclick=()=>{CFB_DEMO_STATE.conference=btn.dataset.conference;cfbRender(parentElement);};
  }
  const reset=area.querySelector("#abiq-cfb-reset");
  reset.onclick=()=>{
    delete CFB_DEMO_STATE.byConference[conference];
    cfbRender(parentElement);
  };
  const weekSelect=area.querySelector("#abiq-cfb-week");
  weekSelect.replaceChildren();
  for(let w=1;w<=CFB_WEEKS;w++){
    const option=cfbNode("option","",`Week ${w}`);
    option.value=String(w);
    weekSelect.appendChild(option);
  }
  weekSelect.value=String(s.week);
  weekSelect.onchange=()=>{s.week=Number(weekSelect.value);cfbRender(parentElement);};

  area.querySelector("#abiq-cfb-week-heading").textContent="WEEK "+s.week;
  const notice=area.querySelector("#abiq-cfb-notice");
  notice.textContent=s.message || "Try an alternate weekly pick to see the ripple effect across the season.";
  const metrics=area.querySelector("#abiq-cfb-metrics");
  metrics.replaceChildren(
    cfbMetric("FULL-SEASON PATH","14 weeks","One survivor selection every week"),
    cfbMetric("TEAMS RESERVED","14 / "+fixture.names.length,"No team reused within this conference"),
    cfbMetric("ILLUSTRATIVE PICK AVERAGE",cfbPercent(s.average),"Example inputs only · not model performance")
  );

  // A weekly recommendation is ranked by its best feasible full-season path,
  // not by win percentage alone. This also excludes previously used teams.
  const otherLocks={...s.locks};
  delete otherLocks[s.week];
  for(let w=1;w<s.week;w++) otherLocks[w]=s.path[w];
  const ranked=fixture.names.map(team=>fixture.byTeam[team][s.week-1])
    .filter(Boolean)
    .map(option=>{
      const trial=cfbOptimize(conference,{...otherLocks,[s.week]:option.team});
      if(trial.error) return null;
      const strategyScore=Object.entries(trial.path).reduce((sum,[week,team])=>
        sum+Math.log(fixture.byTeam[team][Number(week)-1].probability),0);
      return {...option,strategyScore};
    })
    .filter(Boolean)
    .sort((a,b)=>b.strategyScore-a.strategyScore || b.probability-a.probability);
  const currentTeam=s.path[s.week];
  const shortlist=ranked.slice(0,5);
  if(!shortlist.some(option=>option.team===currentTeam)) {
    shortlist.pop();
    shortlist.push(cfbOption(s.week,currentTeam));
  }
  const picks=area.querySelector("#abiq-cfb-picks");
  picks.replaceChildren();
  for(const [index,option] of shortlist.entries()) {
    const isCurrent=option.team===currentTeam;
    const button=cfbNode("button","abiq-cfb-pick"+(isCurrent?" selected":""));
    button.type="button";
    button.setAttribute("aria-label","Select "+option.team+" for Week "+s.week);
    button.append(
      cfbNode("span","abiq-cfb-pick-rank",index+1),
      (()=>{const c=cfbNode("span","abiq-cfb-pick-team");c.append(
        cfbNode("strong","",option.team),
        cfbNode("small","",(option.home?"vs ":"@ ")+option.opponent)
      );return c;})(),
      cfbNode("span","abiq-cfb-pick-prob",cfbPercent(option.probability)),
      cfbNode("span","abiq-cfb-pick-action",isCurrent?(s.locks[s.week]?"LOCKED":"IN PATH"):"TRY PICK ›")
    );
    button.onclick=()=>{cfbOverride(s.week,option.team);cfbRender(parentElement);};
    const future=fixture.byTeam[option.team].filter(g=>g && g.week>s.week);
    const bestFuture=future.length?Math.max(...future.map(g=>g.probability)):null;
    const read=bestFuture && bestFuture>option.probability+.045
      ? "Save-for-later signal: a stronger illustrative matchup is available in a future week."
      : "Competitive current-week option; availability elsewhere still shapes the season path.";
    const note=cfbNode("div","abiq-cfb-pick-note",read);
    picks.append(button,note);
  }

  const impact=area.querySelector("#abiq-cfb-impact");
  impact.replaceChildren();
  impact.append(cfbNode("h4","abiq-cfb-impact-head",s.changes.length
    ? s.changes.length+" downstream "+(s.changes.length===1?"change":"changes")
    : "Optimize beyond this week."));
  impact.append(cfbNode("p","abiq-cfb-impact-sub",s.changes.length
    ? "The highlighted weeks below now use different teams because of your manual selection."
    : "Pick a different team this week and ABIQ rebuilds the rest of the illustrative season rather than simply swapping one card."));
  const changeList=cfbNode("div","abiq-cfb-impact-list");
  for(const change of s.changes.slice(0,6)) {
    const line=cfbNode("div","abiq-cfb-change");
    line.append(cfbNode("span","","WK "+change.week),
      cfbNode("strong","",change.before+"  →  "+change.after));
    changeList.appendChild(line);
  }
  if(s.changes.length>6) changeList.append(cfbNode("div","abiq-cfb-impact-sub","+"+(s.changes.length-6)+" other changed weeks; all are visible in the season outlook."));
  impact.append(changeList);

  const season=area.querySelector("#abiq-cfb-season-grid");
  season.replaceChildren();
  for(let w=1;w<=CFB_WEEKS;w++){
    const team=s.path[w], game=fixture.byTeam[team][w-1];
    const button=cfbNode("button","abiq-cfb-week-card"+
      (w===s.week?" active":"")+
      (s.changes.some(c=>c.week===w)?" changed":""));
    button.type="button";
    button.setAttribute("aria-label","View Week "+w+" survivor recommendations");
    button.append(
      cfbNode("span","","WEEK "+w),
      cfbNode("strong","",team),
      cfbNode("small","",(game.home?"vs ":"@ ")+game.opponent+" · "+cfbPercent(game.probability))
    );
    if(s.locks[w]) button.append(cfbNode("em","","MANUAL PICK"));
    else if(s.changes.some(c=>c.week===w)) button.append(cfbNode("em","","REOPTIMIZED"));
    button.onclick=()=>{s.week=w;cfbRender(parentElement);};
    season.appendChild(button);
  }

  const teamSelect=area.querySelector("#abiq-cfb-team");
  teamSelect.replaceChildren();
  for(const team of fixture.names) {
    const option=cfbNode("option","",team);
    option.value=team;
    teamSelect.appendChild(option);
  }
  if(!fixture.byTeam[s.team]) s.team=s.path[s.week];
  teamSelect.value=s.team;
  teamSelect.onchange=()=>{s.team=teamSelect.value;cfbRender(parentElement);};

  const games=fixture.byTeam[s.team];
  const inPath=Object.keys(s.path).find(week=>s.path[week]===s.team);
  const selectedWeek=inPath?Number(inPath):null;
  area.querySelector("#abiq-cfb-team-summary").textContent =
    s.team+" · 12 illustrated games and 2 bye weeks · "+
    (selectedWeek?"reserved for Week "+selectedWeek:"not currently reserved in this path");
  const table=cfbNode("table","abiq-cfb-table");
  const thead=cfbNode("thead","");
  const heads=cfbNode("tr","");
  for(const title of ["WEEK","MATCHUP","DEMO WIN CHANCE","SEASON STATUS"]) heads.append(cfbNode("th","",title));
  thead.append(heads);table.append(thead);
  const tbody=cfbNode("tbody","");
  for(let w=1;w<=CFB_WEEKS;w++){
    const game=games[w-1];
    const tr=cfbNode("tr",s.path[w]===s.team?"in-plan":"");
    tr.append(cfbNode("td","","W"+w));
    if(!game){
      tr.append(cfbNode("td","","BYE"),cfbNode("td","","—"),cfbNode("td","","No game"));
    } else {
      tr.append(cfbNode("td","",(game.home?"vs ":"@ ")+game.opponent),
        cfbNode("td","",cfbPercent(game.probability)));
      const status=cfbNode("td","");
      if(s.path[w]===s.team) status.append(cfbNode("strong","","IN PATH"));
      else {
        const tryButton=cfbNode("button","abiq-cfb-table-pick","TRY WEEK "+w);
        tryButton.type="button";
        tryButton.onclick=()=>{
          if(cfbOverride(w,s.team)) s.week=w;
          cfbRender(parentElement);
        };
        status.append(tryButton);
      }
      tr.append(status);
    }
    tbody.append(tr);
  }
  table.append(tbody);
  area.querySelector("#abiq-cfb-schedule-table").replaceChildren(table);
}

// Add the new page without changing the frozen NFL Dashboard/Forecasts renderers.
ICONS.survivor = `<svg viewBox="0 0 24 24"><path d="M12 3 4 7v5c0 5.5 3.5 8.8 8 10 4.5-1.2 8-4.5 8-10V7z"></path><path d="m8 12 2.5 2.5 5-5"></path></svg>`;
NAV_ITEMS.splice(2,0,["CFB Survivor","survivor"]);
const cfbOriginalInitialize = initialize;
initialize = function(component) {
  cfbOriginalInitialize(component);
  cfbRender(component.parentElement);
};
const cfbOriginalSetPage = setPage;
setPage = function(parentElement,pageName) {
  cfbOriginalSetPage(parentElement,pageName);
  parentElement.querySelector("#abiq-dashboard-root")?.classList.toggle("abiq-cfb-active",pageName==="CFB Survivor");
};
