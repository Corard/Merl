// Goal Variables
let fieldData;
let goals;
let goalID = 0;
let totalBits = 0;
let tmpGoal;
const goalsField = "goalsField";

// Countdown Variables
let minTimer = new Date();
let maxTimer = new Date();
let start;

function onWidgetLoad(obj)
{
  fieldData = obj.detail.fieldData;
  console.clear()
  console.log(`Widget Load:\n${JSON.stringify(obj)}\n`);
  // Goal Initialisation
  goals = fieldData.goalsField;
  console.log(`Goals:\n${JSON.stringify(goals)}\n`);
  renderOverlay();
  resetCountdown();
}

function onSessionUpdate(obj)
{
  console.log(`Session Load:\n${JSON.stringify(obj)}\n`);
}

function onCheer(data)
{
  totalBits += data.amount; // Add bits amount to the totalBits counter
  console.log(`Cheer Event:\n${JSON.stringify(data)}\n`); // Log the cheer event
  console.log(`Total Bits: ${totalBits}\n`); // Log the total bits
  checkProgress();
}

function onWidgetButton(data)
{
  console.log(`Widget Button:\n${JSON.stringify(data)}\n`);
  if (data.field === "resetButton") {
    // Reset Goals
  	goalID = 0;
	totalBits = 0;
    renderOverlay();
    resetCountdown();
  } else if (data.field === "checkProgress") {
    checkProgress();
  }
}

function onKVStoreUpdate(data)
{
  console.log(`KV Store Update:\n${JSON.stringify(data)}\n`);
}

function checkProgress()
{
  if (goals[goalID].goal == undefined) {
    tmpGoal = 999;
  } else {
    tmpGoal = goals[goalID].goal;
  }
  if (totalBits < tmpGoal) {
    renderOverlay();
  } else if (totalBits >= tmpGoal) {
    while (totalBits >= tmpGoal) {
      console.log(`Goal Hit: ${goals[goalID].description}`)
      if (goals[goalID].description === "Add an Extra 6 Hours") {
        countdown(21600) // +6 Hours
      }
      goalID++;
      renderOverlay();
    }
  }
  console.log(`Ran Check Progress!\n  Total Bits: ${totalBits}\n  Goal Amount: ${tmpGoal}\n  Goal Description: ${goals[goalID].description}`);
}

function renderOverlay()
{
  console.log(`Goal: ${goals[goalID].goal}`);
  if (goals[goalID].goal == undefined) {
    tmpGoal = 1000;
  } else {
    tmpGoal = goals[goalID].goal;
  }
  document.getElementById("current").innerHTML = goals[goalID].description; // goals[goalID].description
  document.getElementById("next").innerHTML = goals[goalID+1].description; // goals[goalID+1].description
  document.getElementById("progress").innerHTML = `${totalBits}/${tmpGoal}`; // ${totalBits}/${goals[goalID].goal}
}

function resetCountdown()
{
  // Countdown Initialisation
  minTimer = new Date();
  minTimer.setMinutes(minTimer.getMinutes() + fieldData.minTimer);
  maxTimer = new Date();
  maxTimer.setMinutes(maxTimer.getMinutes() + fieldData.maxTimer);
  start = minTimer;
  countdown(1);
}

function countdown(seconds)
{
  if (seconds == 0) {
    return;
  }
  let toCountDown = start;
  toCountDown.setSeconds(toCountDown.getSeconds() + seconds);
  $('#countdown').countdown(toCountDown, function (event) {
    if (event.type === "finish") $(this).html(fieldData.onCompleter);
    else $(this).html(event.strftime('%I:%M:%S'));
  });
}