# figma2vuejs

![Status](https://img.shields.io/badge/status-development_phase-orange) ![Stability](https://img.shields.io/badge/stability-incomplete%20coverage-yellow)

figma2vuejs is a tool that generates front-end Vue.js code projects from Figma prototypes of the user interface. The aim of this approach is to generate code that can be easily integrated into the overall application development, reducing therefore the gap between the design phase and the implementation phase.

## Nomenclatures and component-based prototyping

Since frames in the first level of the Figma artboard can represent state variations, such as hovering or overlay elements, in order to consider a given node as a Vue page, do the following:

- *Insert "#Page" at the end of a Frame's node name to convert it as a Vue page.*

These are the following components from our design-system that you can import to your Figma prototypes (the component's nomenclatures are reserved) to explore better logic implementation on the final Vue.js code (<a href="https://www.figma.com/design/MyaEF410LKOiWImiuWwbUR/figma2vuejs?node-id=0-1&t=Ej93UKX9vtl9Djiy-1">click here</a> to explore and import them). The components from our design system built until now consist on the:
- *InputSearch, DatePicker, Dropdown, ReadOnlyRating, InteractiveRating, Paginator, Form, Checkbox, Menu, Slider, Table.*

<img src="tool-overview/figmadesignsystem.png" width="450" />

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

## Publication 

>*João Peixoto Castro and José Creissac Campos* (October, 2025). **Automating code generation from User Interface prototypes**. In 2025. International Conference on Graphics and Interaction (ICGI) (pp. 1-8). IEEE. DOI: XXXXXXX