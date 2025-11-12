from vertexai.preview.generative_models import GenerativeModel
import vertexai
import os
import json
import logging
import re

logging.basicConfig(filename="ai_debug.log", level=logging.INFO)

vertexai.init(project=os.getenv("GCP_PROJECT_ID"), location=os.getenv("GCP_LOCATION"))

def parse_estimation(raw_text: str):
    """You are a senior structural steel estimator AI with 20+ years of experience.
You specialize in reading engineering drawings, fabrication details, and general notes.

Your goal is to analyze the given text extracted from an engineering drawing (OCR output)
and extract relevant structural information such as beams, columns, plates, foundations,
and reinforcement data.


Follow these strict rules:

1. Identify components:
   - Beam
   - Column
   - Plate (base plate, gusset, connection plate, stiffener)
   - Foundation or footing
   - Reinforcement (bars, mesh, cages)
   - Bolt or connection information

2. Extract measurable attributes if present:
   - Dimensions (width, height, thickness, length, depth)
   - Unit (mm, inches, feet)
   - Material (Steel, Concrete, Rebar)
   - Quantity (e.g., “2 PLATES”, “(4) BARS”)
   - Type or grade (e.g., “A325”, “A36”, “Fe500”)
   - Connection type (e.g., “Beam to Beam”, “Column to Base Plate”)

3. Normalize units:
   - Convert all inches to millimeters (1 inch = 25.4 mm)
   - Convert all feet and inches (e.g., 2'-6") to millimeters
   - Return all numeric fields as numbers (not strings)
 make use of the scale provided in the drawing text if available to cal culate the columns height
4. If dimension or data is missing, return 0 or null but include the component type.

5. Return data as **valid JSON array**, strictly matching this schema:

[
  {
    "type": "ComponentType",
    "material": "Steel | Concrete | Rebar",
    "width_mm": number,
    "height_mm": number,
    "thickness_mm": number,
    "length_mm": number,
    "depth_mm": number,
    "quantity": number,
    "connection": "string",
    "grade": "string",
    "notes": "string"
  }
]

6. Only include relevant structural or connection elements — ignore unrelated text (titles, sheet scales, drawing numbers).

7. Output **only JSON**, no markdown, no explanation.

Example conversions:
Input:
"BEAM TO COLUMN CONNECTION, 2″ THK PL, (4) A325 BOLTS, W12x26 BEAM, SEE PLAN"
Output:
[
  {
    "type": "Beam",
    "material": "Steel",
    "width_mm": 305,
    "height_mm": 660,
    "thickness_mm": 50.8,
    "quantity": 1,
    "connection": "Beam to Column",
    "grade": "A325",
    "notes": "See plan"
  }
]
"""
    if not raw_text or len(raw_text.strip()) < 20:
        logging.warning("Raw text too short for estimation")
        return []

    model = GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""Analyze this engineering drawing OCR text and extract structured data:
    
{raw_text}

Return ONLY valid JSON array with these fields:
- type: component type (e.g., "Plate", "Bolt", "Beam")
- thickness_in: thickness in inches (number or null)
- width_in: width in inches (number or null)
- height_in: height in inches (number or null)
- material: material type (string)
- quantity: quantity (number or null)
- cost: estimated cost (number or null)

Example format:
[
  {{"type": "Plate", "thickness_in": 2.0, "material": "Steel", "quantity": 1}},
  {{"type": "Bolt", "material": "A325", "quantity": 2}}
]

Return ONLY the JSON array, no markdown formatting, no extra text."""

    response = model.generate_content(prompt)
    raw_output = response.text
    logging.info(f"Gemini raw output: {raw_output}")
    
    # Extract JSON from markdown code blocks if present
    json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', raw_output, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        json_str = raw_output
    
    try:
        parsed_data = json.loads(json_str)
        logging.info(f"Successfully parsed: {parsed_data}")
        return parsed_data if isinstance(parsed_data, list) else [parsed_data]
    except json.JSONDecodeError as e:
        logging.error(f"JSON parse error: {e}")
        logging.error(f"Attempted to parse: {json_str}")
        return []
