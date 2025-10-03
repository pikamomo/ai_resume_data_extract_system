__all__ = [
    "ContactInfo",
    "EducationItem",
    "ExperienceItem",
    "CertificationItem",
    "Resume",
]    

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class ContactInfo(BaseModel):
    name: Optional[str] = Field(default=None, description="Full candidate name")
    email: Optional[str] = Field(default=None, description="Primary email address")
    phone: Optional[str] = Field(default=None, description="Primary phone number")
    location: Optional[str] = Field(default=None, description="City, State or City, Country")
    linkedin: Optional[HttpUrl] = Field(default=None, description="LinkedIn profile URL")
    github: Optional[HttpUrl] = Field(default=None, description="GitHub profile URL")
    website: Optional[HttpUrl] = Field(default=None, description="Personal website or portfolio URL")


class Education(BaseModel):
    institution: Optional[str] = Field(default=None)
    degree: Optional[str] = Field(default=None, description="Degree name e.g., Bachelor of Science")
    field_of_study: Optional[str] = Field(default=None, description="Major/Concentration")
    start_date: Optional[str] = Field(default=None, description="Start date, free-form string")
    end_date: Optional[str] = Field(default=None, description="End date or Present")
    gpa: Optional[str] = Field(default=None)


class Experience(BaseModel):
    company: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None, description="Bullets or paragraph of responsibilities/impact")


class Certification(BaseModel):
    name: str
    issuer: Optional[str] = None
    date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None


class Resume(BaseModel):
    contact: ContactInfo = Field(default_factory=ContactInfo)
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)