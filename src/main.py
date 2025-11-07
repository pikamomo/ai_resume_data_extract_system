from pathlib import Path
from typing import List, Dict, Optional
import json
import os
from datetime import datetime

from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv, find_dotenv

from models.resume import Resume


class ResumeProcessor:
    """Elegant batch processor for resume PDF files."""
    
    def __init__(self, model_name: str = 'gpt-4o-mini', model_provider: str = 'openai'):
        load_dotenv(find_dotenv())
        self.model = init_chat_model(
            model=model_name, 
            model_provider=model_provider
        ).with_structured_output(Resume, method="function_calling")
        
        self.prompt_template = PromptTemplate(
            template="""
            You are an AI assistant tasked with extracting structured information from a resume.
            
            Only extract information that's present in the Resume class.
            
            Resume Context:
            {resume_text}
            """,
            input_variables=["resume_text"]
        )
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Load and extract text from a PDF file."""
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        return "\n".join([doc.page_content for doc in docs])
    
    def process_single_resume(self, pdf_path: Path) -> Optional[Dict]:
        """Process a single resume PDF and return structured data."""
        try:
            print(f"  📄 Processing: {pdf_path.name}")
            
            # Extract text from PDF
            resume_text = self.extract_text_from_pdf(pdf_path)
            
            # Generate prompt and invoke model
            prompt = self.prompt_template.invoke({'resume_text': resume_text})
            response = self.model.invoke(prompt)
            
            # Convert to dictionary
            result = response.model_dump()
            result['source_file'] = pdf_path.name
            result['processed_at'] = datetime.now().isoformat()
            
            print(f"  ✓ Successfully processed: {pdf_path.name}")
            return result
            
        except Exception as e:
            print(f"  ✗ Error processing {pdf_path.name}: {str(e)}")
            return None
    
    def process_batch(self, resume_folder: Path, output_folder: Path) -> None:
        """Process all PDF files in the resume folder."""
        # Create output directory if it doesn't exist
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Find all PDF files
        pdf_files = list(resume_folder.glob('*.pdf'))
        
        if not pdf_files:
            print(f"⚠ No PDF files found in {resume_folder}")
            return
        
        print(f"\n{'='*60}")
        print(f"🚀 Starting Batch Resume Processing")
        print(f"{'='*60}")
        print(f"📁 Input Folder: {resume_folder}")
        print(f"📂 Output Folder: {output_folder}")
        print(f"📊 Total Resumes: {len(pdf_files)}\n")
        
        results = []
        successful = 0
        failed = 0
        
        # Process each PDF
        for idx, pdf_path in enumerate(pdf_files, 1):
            print(f"\n[{idx}/{len(pdf_files)}]")
            result = self.process_single_resume(pdf_path)
            
            if result:
                results.append(result)
                successful += 1
                
                # Save individual result
                output_file = output_folder / f"{pdf_path.stem}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, indent=2, ensure_ascii=False, fp=f)
            else:
                failed += 1
        
        # Save consolidated results
        if results:
            consolidated_file = output_folder / 'all_resumes.json'
            with open(consolidated_file, 'w', encoding='utf-8') as f:
                json.dump(results, indent=2, ensure_ascii=False, fp=f)
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"✅ Batch Processing Complete!")
        print(f"{'='*60}")
        print(f"✓ Successful: {successful}")
        print(f"✗ Failed: {failed}")
        print(f"📁 Results saved to: {output_folder}")
        print(f"{'='*60}\n")


def main():
    """Main entry point for batch resume processing."""
    # Define paths
    resume_folder = Path('resume')
    output_folder = Path('output')
    
    # Initialize processor
    processor = ResumeProcessor()
    
    # Process all resumes
    processor.process_batch(resume_folder, output_folder)


if __name__ == "__main__":
    main()
