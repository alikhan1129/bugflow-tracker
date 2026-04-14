from backend.models import db, Bug
from backend.schemas import BugCreate, BugUpdate
from backend.ai_service import ai_service

class BugService:
    @staticmethod
    def create_bug(data: BugCreate) -> Bug:
        severity, category, title = None, None, data.title
        
        if data.use_ai_triage:
            triage = ai_service.triage_bug(data.title, data.description)
            severity, category, title = triage.severity, triage.category, triage.title

        bug = Bug(title=title, description=data.description, severity=severity, category=category)
        db.session.add(bug)
        db.session.commit()
        return bug

    @staticmethod
    def get_all_bugs():
        return Bug.query.order_by(Bug.created_at.desc()).all()

    @staticmethod
    def update_bug(bug_id: int, data: BugUpdate) -> Bug:
        bug = Bug.query.get_or_404(bug_id)
        
        if data.status:
            flow = {'OPEN': ['IN_PROGRESS'], 'IN_PROGRESS': ['RESOLVED'], 'RESOLVED': ['CLOSED']}
            new_status = data.status.upper()
            if new_status not in flow.get(bug.status, []):
                raise ValueError(f"Invalid transition from {bug.status}")
            if new_status == 'CLOSED' and not data.resolution_notes:
                raise ValueError("Notes required to close")
            bug.status = new_status
            
        if data.resolution_notes:
            bug.resolution_notes = data.resolution_notes
            
        db.session.commit()
        return bug

bug_service = BugService()
