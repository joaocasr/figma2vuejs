# figma2vuejs

![Status](https://img.shields.io/badge/status-development_phase-orange) ![Stability](https://img.shields.io/badge/stability-incomplete%20coverage-yellow)

figma2vuejs is a MBUID tool that let's you convert figma prototypes into fully functional Vue.js projects.

## Nomenclatures and component-based prototyping
- *Insert "#Page" at the end of a Frame's node name to convert as a Vue page.*

Components from our design-system that you can import to your prototypes (reserved node's nomenclature):
- *InputSearch, DatePicker, Dropdown, ReadOnlyRating, InteractiveRating, Paginator, Form, Checkbox, Menu, Slider, Table.*

<img src="tool-overview/figmadesignsystem.png" width="450" />

<a href="https://www.figma.com/design/MyaEF410LKOiWImiuWwbUR/figma2vuejs?node-id=0-1&t=Ej93UKX9vtl9Djiy-1">Click Here</a>

## Setup
Setup commands to run the backend
```bash
git clone https://github.com/joaocasr/figma2vuejs
cd figma2vuejs/server/src/ && pip install -r requirements.txt
uvicorn figma2vuejs:app # run backend server
```
Setup commands to run the frontend
```bash
cd figma2vuejs/figma2vuejs/
npm install # node version >= 20.19+
npm run build
npm run preview
```
Copty the URL from the Figma prototype you want to convert.

<img src="tool-overview/figmaurl.png" width="500" />

Then generate a Figma token associated with your account (Settings tab).  

<img src="tool-overview/figmatoken.png" width="500" />

Finnaly, insert those credentials in the Figma2Vuejs webpage and press generate.  

<img src="tool-overview/figma2vuejs.png" width="500" />


