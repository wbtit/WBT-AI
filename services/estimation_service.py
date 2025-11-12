from .vision_service import extract_text
from .vertex_estimation_service import parse_estimation
from models.estimation_model import Estimation
from sqlmodel import Session
import logging

logging.basicConfig(filename="ai_debug.log", level=logging.INFO)

def run_ai_estimation(file_path: str, drawing_id: int, session: Session):
    """Full AI pipeline: OCR → Gemini → structured estimation → DB save."""
    print(f"🧠 Running AI estimation for file: {file_path}")
    
    raw_text = extract_text(file_path)
    if not raw_text or len(raw_text.strip()) < 20:
        logging.warning(f"No sufficient text extracted from {file_path}")
        return []

    structured_data = parse_estimation(raw_text)
    logging.info(f"Structured data returned: {structured_data}")

    # Save to database
    estimations = []
    if isinstance(structured_data, list) and len(structured_data) > 0:
        for item in structured_data:
            try:
                estimation = Estimation(
                    drawing_id=drawing_id,
                    category=item.get("type", "Unknown"),
                    width=float(item.get("width_in", 0.0)) if item.get("width_in") else 0.0,
                    height=float(item.get("height_in", 0.0)) if item.get("height_in") else 0.0,
                    material=item.get("material", "Unknown"),
                    cost=float(item.get("cost")) if item.get("cost") else None
                )
                session.add(estimation)
                estimations.append(estimation)
                logging.info(f"Created estimation: {estimation}")
            except Exception as e:
                logging.error(f"Error creating estimation: {e}")
                continue
        
        try:
            session.commit()
            logging.info(f"✅ Saved {len(estimations)} estimations for drawing {drawing_id}")
        except Exception as e:
            logging.error(f"Error committing estimations: {e}")
            session.rollback()
            return []
    else:
        logging.warning(f"No structured data to save: {structured_data}")
    
    return estimations
