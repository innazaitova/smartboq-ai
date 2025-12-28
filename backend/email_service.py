"""
Email Service Module
Handles sending emails via SendGrid for welcome emails, notifications, etc.
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Email service using SendGrid"""
    
    def __init__(self):
        self.api_key = os.getenv("SENDGRID_API_KEY")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@smartboq.ai")
        self.from_name = os.getenv("FROM_NAME", "SmartBOQ AI")
        
        if not self.api_key:
            logger.warning("SENDGRID_API_KEY not set - email functionality disabled")
            self.enabled = False
        else:
            self.client = SendGridAPIClient(self.api_key)
            self.enabled = True
            logger.info("Email service initialized successfully")
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_content: Optional[str] = None
    ) -> bool:
        """
        Send an email via SendGrid
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email body
            plain_content: Plain text fallback (optional)
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            logger.warning(f"Email service disabled - skipping email to {to_email}")
            return False
        
        try:
            message = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(to_email),
                subject=subject,
                plain_text_content=Content("text/plain", plain_content or html_content),
                html_content=Content("text/html", html_content)
            )
            
            response = self.client.send(message)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully to {to_email}: {subject}")
                return True
            else:
                logger.error(f"Failed to send email to {to_email}: Status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}", exc_info=True)
            return False
    
    async def send_welcome_email(self, to_email: str, full_name: str) -> bool:
        """Send welcome email to newly registered user"""
        subject = "Welcome to SmartBOQ AI! 🚀"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ background: #667eea; color: white; padding: 12px 30px; 
                          text-decoration: none; border-radius: 5px; display: inline-block; 
                          margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                .feature {{ background: white; padding: 15px; margin: 10px 0; 
                           border-left: 4px solid #667eea; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to SmartBOQ AI!</h1>
                    <p>AI-Powered Construction Quantity Surveying</p>
                </div>
                <div class="content">
                    <h2>Hello {full_name}! 👋</h2>
                    <p>Thank you for joining SmartBOQ AI - the future of construction cost estimation.</p>
                    
                    <p>Your account has been successfully created and you're ready to start transforming your construction drawings into accurate Bill of Quantities.</p>
                    
                    <div class="feature">
                        <strong>🎯 What you can do now:</strong>
                        <ul>
                            <li>Upload construction drawings (PDF, DWG, PNG)</li>
                            <li>Create and manage projects</li>
                            <li>Get AI-powered quantity takeoffs</li>
                            <li>Generate professional BOQs</li>
                        </ul>
                    </div>
                    
                    <div class="feature">
                        <strong>🎁 Trial Account Benefits:</strong>
                        <ul>
                            <li>Process up to 5 drawings</li>
                            <li>3 active projects</li>
                            <li>Basic AI analysis</li>
                            <li>Export to Excel/PDF</li>
                        </ul>
                    </div>
                    
                    <center>
                        <a href="https://smartboq-ai.vercel.app/dashboard" class="button">
                            Go to Dashboard →
                        </a>
                    </center>
                    
                    <p>Need help getting started? Check out our <a href="https://smartboq-ai.vercel.app/features">features guide</a> or <a href="https://smartboq-ai.vercel.app/contact">contact support</a>.</p>
                    
                    <p>Best regards,<br>
                    The SmartBOQ AI Team</p>
                </div>
                <div class="footer">
                    <p>© 2024 SmartBOQ AI. All rights reserved.</p>
                    <p>You're receiving this email because you signed up for SmartBOQ AI.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_content = f"""
        Welcome to SmartBOQ AI!
        
        Hello {full_name},
        
        Thank you for joining SmartBOQ AI - the future of construction cost estimation.
        
        Your account has been successfully created and you're ready to start transforming 
        your construction drawings into accurate Bill of Quantities.
        
        What you can do now:
        - Upload construction drawings (PDF, DWG, PNG)
        - Create and manage projects
        - Get AI-powered quantity takeoffs
        - Generate professional BOQs
        
        Trial Account Benefits:
        - Process up to 5 drawings
        - 3 active projects
        - Basic AI analysis
        - Export to Excel/PDF
        
        Get started: https://smartboq-ai.vercel.app/dashboard
        
        Need help? Contact us: https://smartboq-ai.vercel.app/contact
        
        Best regards,
        The SmartBOQ AI Team
        """
        
        return await self.send_email(to_email, subject, html_content, plain_content)
    
    async def send_project_created_email(
        self,
        to_email: str,
        full_name: str,
        project_name: str,
        project_id: int
    ) -> bool:
        """Send notification when project is created"""
        subject = f"Project Created: {project_name}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2>Project Created Successfully! ✅</h2>
                <p>Hello {full_name},</p>
                <p>Your project <strong>"{project_name}"</strong> has been created successfully.</p>
                <p>Next steps:</p>
                <ul>
                    <li>Upload your construction drawings</li>
                    <li>Our AI will analyze and extract quantities</li>
                    <li>Review and export your BOQ</li>
                </ul>
                <a href="https://smartboq-ai.vercel.app/projects/{project_id}" 
                   style="background: #667eea; color: white; padding: 12px 30px; 
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    View Project →
                </a>
                <p style="margin-top: 20px;">Best regards,<br>SmartBOQ AI Team</p>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_drawing_processed_email(
        self,
        to_email: str,
        full_name: str,
        project_name: str,
        project_id: int,
        elements_detected: int
    ) -> bool:
        """Send notification when drawing processing is complete"""
        subject = f"Drawing Processed: {project_name}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2>Drawing Processing Complete! 🎉</h2>
                <p>Hello {full_name},</p>
                <p>Your drawings for <strong>"{project_name}"</strong> have been processed successfully.</p>
                <p><strong>{elements_detected} construction elements</strong> were detected and quantified.</p>
                <a href="https://smartboq-ai.vercel.app/projects/{project_id}" 
                   style="background: #667eea; color: white; padding: 12px 30px; 
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    View Results →
                </a>
                <p style="margin-top: 20px;">Best regards,<br>SmartBOQ AI Team</p>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)


# Global email service instance
email_service = EmailService()
