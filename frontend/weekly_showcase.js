/* Mixed weekly Showcase board.
   Frozen public NFL Week 1 selections and constructed CFB survivor scenarios are
   deliberately separated by source. No live forecasts or provider calls. */
const ABIQ_WEEKLY_DASHBOARD = {week:1, data:null, parentElement:null};

function abiqWeeklyRows(week, data) {
  if (!Number.isInteger(week) || week<1 || week>CFB_WEEKS) return [];
  const rows=[];
  if (week===1) {
    for (const pick of (data.recommendations ?? []).slice(0,3)) {
      rows.push({sport:"NFL",conference:null,team:pick.team,opponent:pick.opponent,
        probability:pick.probability,confidence:pick.confidence,illustrative:false});
    }
  }
  for(const conference of ["SEC","BIG TEN"]) {
    const scenario=cfbScenario(conference);
    const team=scenario.path[week];
    const game=CFB_FIXTURES[conference].byTeam[team][week-1];
    if (!game) throw new Error("CFB season scenario has an unavailable Week "+week+" matchup.");
    rows.push({sport:"CFB",conference,team,opponent:game.opponent,
      home:game.home,probability:cfbPercent(game.probability),
      illustrative:true,manual:scenario.locks[week]===team});
  }
  return rows;
}

// DOM integration, after the pure board selection contract above.
function abiqWeeklyElement(tag,cls,text) {
  const node=document.createElement(tag);
  if (cls) node.className=cls;
  if (text!==undefined) node.textContent=String(text);
  return node;
}

function abiqWeeklyCard(row) {
  const card=abiqWeeklyElement("article","abiq-weekly-card abiq-surface");
  const head=abiqWeeklyElement("div","abiq-weekly-card-head");
  head.append(
    abiqWeeklyElement("span","abiq-weekly-source",row.sport==="NFL"?"NFL · FROZEN SNAPSHOT":row.conference+" · SURVIVOR DEMO"),
    abiqWeeklyElement("span","abiq-weekly-label",row.sport==="NFL"?row.confidence+" tier":(row.manual?"MANUAL PATH":"OPTIMAL PATH"))
  );
  const matchup=abiqWeeklyElement("div","abiq-weekly-matchup");
  const logos=abiqWeeklyElement("div","abiq-weekly-logos");
  if(row.sport==="NFL") {
    for(const team of [row.team,row.opponent]) {
      const img=abiqWeeklyElement("img");
      img.src=teamLogo(team);
      img.alt=team+" logo";
      img.loading="lazy";
      logos.append(img);
    }
  } else {
    logos.append(cfbLogoNode(row.team),cfbLogoNode(row.opponent));
  }
  const names=abiqWeeklyElement("div","abiq-weekly-names");
  names.append(
    abiqWeeklyElement("strong","",row.team),
    abiqWeeklyElement("small","",(row.sport==="CFB"?(row.home?"vs ":"@ "):"vs ")+row.opponent)
  );
  matchup.append(logos,names);
  const forecast=abiqWeeklyElement("div","abiq-weekly-probability");
  forecast.append(
    abiqWeeklyElement("strong","",row.probability),
    abiqWeeklyElement("span","",row.illustrative?"Illustrative win chance":"Frozen model forecast")
  );
  const action=abiqWeeklyElement("button","abiq-weekly-open",row.sport==="NFL"?"VIEW NFL FORECASTS  ›":"EXPLORE "+row.conference+"  ›");
  action.type="button";
  action.onclick=()=>{
    const root=ABIQ_WEEKLY_DASHBOARD.parentElement;
    if(row.sport==="NFL") {
      setPage(root,"Forecasts");
    } else {
      CFB_DEMO_STATE.conference=row.conference;
      cfbScenario(row.conference).week=ABIQ_WEEKLY_DASHBOARD.week;
      cfbRender(root);
      setPage(root,"CFB Survivor");
    }
  };
  card.append(head,matchup,forecast,action);
  return card;
}

function abiqWeeklyRender() {
  const {parentElement,data,week}=ABIQ_WEEKLY_DASHBOARD;
  if(!parentElement || !data) return;
  const panel=parentElement.querySelector("#abiq-weekly-command");
  if(!panel) return;
  const all=abiqWeeklyRows(week,data);
  panel.querySelector("#abiq-weekly-week").textContent="WEEK "+week;
  panel.querySelector("#abiq-weekly-nfl-title").textContent=week===1?"NFL · Frozen Week 1 example":"NFL · No snapshot for Week "+week;
  const nfl=panel.querySelector("#abiq-weekly-nfl-picks");
  nfl.replaceChildren();
  const nflRows=all.filter(row=>row.sport==="NFL");
  if(nflRows.length) nfl.append(...nflRows.map(abiqWeeklyCard));
  else nfl.append(abiqWeeklyElement("div","abiq-weekly-empty",
    "NFL forecasts for this week are not part of the frozen public Showcase. No later-week predictions have been fabricated."));
  const cfb=panel.querySelector("#abiq-weekly-cfb-picks");
  cfb.replaceChildren(...all.filter(row=>row.sport==="CFB").map(abiqWeeklyCard));
  panel.querySelector("#abiq-weekly-summary").textContent=week===1
    ?"3 frozen NFL forecast examples + 2 interactive CFB survivor selections"
    :"2 interactive CFB survivor selections · No NFL forecast issued in this public sample";
}

function abiqWeeklyInitialize(component) {
  const {parentElement,data}=component;
  ABIQ_WEEKLY_DASHBOARD.parentElement=parentElement;
  ABIQ_WEEKLY_DASHBOARD.data=data;
  const root=parentElement.querySelector("#abiq-dashboard-root");
  if(!root) return;
  root.classList.add("abiq-dashboard-active");
  // Keep the NFL payload frozen; week selection only changes local CFB demos.
  const select=parentElement.querySelector("#abiq-week-select");
  if (select) {
    select.replaceChildren();
    for(let w=1;w<=CFB_WEEKS;w++) {
      const option=document.createElement("option");
      option.value=String(w);
      option.textContent=w===1?"Week 1 · NFL + CFB":"Week "+w+" · CFB demo";
      select.appendChild(option);
    }
    select.value=String(ABIQ_WEEKLY_DASHBOARD.week);
    select.onchange=()=>{
      ABIQ_WEEKLY_DASHBOARD.week=Number(select.value);
      abiqWeeklyRender();
    };
  }
  const nav=parentElement.querySelector('.abiq-nav-item[data-page="Forecasts"] span:last-child');
  if (nav) nav.textContent="NFL Forecasts";
  abiqWeeklyRender();
}

const abiqWeeklyOriginalInitialize=initialize;
initialize=function(component) {
  abiqWeeklyOriginalInitialize(component);
  abiqWeeklyInitialize(component);
};
const abiqWeeklyOriginalSetPage=setPage;
setPage=function(parentElement,pageName) {
  abiqWeeklyOriginalSetPage(parentElement,pageName);
  parentElement.querySelector("#abiq-dashboard-root")?.classList.toggle("abiq-dashboard-active",pageName==="Dashboard");
  if(pageName==="Dashboard") abiqWeeklyRender();
};
