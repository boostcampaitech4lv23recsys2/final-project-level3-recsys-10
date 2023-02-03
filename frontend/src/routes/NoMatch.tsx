import { useCallback } from "react";
import { useNavigate } from "react-router-dom";

export default function NoMatch() {
  const navigate = useNavigate();

  const goBack = useCallback(() => {
    navigate(-1);
  }, [navigate]);
  return (
    <div>
      <button onClick={goBack}> 홈으로 가기</button>
    </div>
  );
}
