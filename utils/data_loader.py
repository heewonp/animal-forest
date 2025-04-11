import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """데이터 로드를 담당하는 클래스"""
    
    @staticmethod
    def load_from_file(file_path):
        """
        파일에서 데이터를 로드
        
        Parameters:
        file_path (str): 데이터 파일 경로
        
        Returns:
        pandas.DataFrame: 로드된 데이터프레임
        """
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                logger.error(f"지원하지 않는 파일 형식: {file_path}")
                return None
                
            logger.info(f"데이터 로드 완료: {len(df)} 행, {len(df.columns)} 열")
            return df
            
        except Exception as e:
            logger.error(f"데이터 로드 중 오류 발생: {e}")
            return None
    
    @staticmethod
    def load_from_uploaded_file(uploaded_file):
        """
        Streamlit에서 업로드된 파일 로드
        
        Parameters:
        uploaded_file: Streamlit의 업로드된 파일 객체
        
        Returns:
        pandas.DataFrame: 로드된 데이터프레임
        """
        try:
            file_type = uploaded_file.name.split('.')[-1].lower()
            
            if file_type == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_type in ['xls', 'xlsx']:
                df = pd.read_excel(uploaded_file)
            else:
                logger.error(f"지원하지 않는 파일 형식: {file_type}")
                return None
                
            logger.info(f"업로드된 데이터 로드 완료: {len(df)} 행, {len(df.columns)} 열")
            return df
            
        except Exception as e:
            logger.error(f"업로드된 데이터 로드 중 오류 발생: {e}")
            return None