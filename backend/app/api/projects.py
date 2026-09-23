from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.base import Location, Project, ProjectSite, User
from backend.app.db.session import get_db
from backend.app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectSiteCreate,
    ProjectSiteResponse,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    owner = db.get(User, project_data.owner_id)

    if not owner:
        raise HTTPException(
            status_code=400,
            detail="Owner user not found",
        )

    if project_data.location_id is not None:
        location = db.get(Location, project_data.location_id)

        if not location:
            raise HTTPException(
                status_code=400,
                detail="Location not found",
            )

    project = Project(**project_data.model_dump())

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.scalars(
        select(Project).order_by(Project.id.desc())
    ).all()


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return project


@router.post(
    "/{project_id}/site",
    response_model=ProjectSiteResponse,
    status_code=201,
)
def create_project_site(
    project_id: int,
    site_data: ProjectSiteCreate,
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    if project.site:
        raise HTTPException(
            status_code=409,
            detail="Project site already exists",
        )

    site = ProjectSite(
        project_id=project_id,
        **site_data.model_dump(),
    )

    db.add(site)
    db.commit()
    db.refresh(site)

    return site


@router.get(
    "/{project_id}/site",
    response_model=ProjectSiteResponse,
)
def get_project_site(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    if not project.site:
        raise HTTPException(
            status_code=404,
            detail="Project site not found",
        )

    return project.site